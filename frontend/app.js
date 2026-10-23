const source = document.querySelector('#source');
const lines = document.querySelector('#lines');
const analyzeButton = document.querySelector('#analyze');
const tokensPanel = document.querySelector('#tokens-panel');
const treePanel = document.querySelector('#tree-panel');
const examples = {
  hello: 'HAI\n\nBTW My first LOLCODE program\nVISIBLE "HAI, WORLD!"\n\nKTHXBYE\n',
  math: 'HAI\n\nWAZZUP\n    I HAS A first ITZ 12\n    I HAS A second ITZ 8\nBUHBYE\n\nVISIBLE "The sum is: " SUM OF first AN second\n\nKTHXBYE\n',
  conditional: 'HAI\n\nBOTH SAEM 5 AN 5\nO RLY?\n    YA RLY\n        VISIBLE "They match!"\n    NO WAI\n        VISIBLE "Try again."\nOIC\n\nKTHXBYE\n'
};
let revision = 0;
let analyzing = false;

function setStatus(title, message, error = false) {
  document.querySelector('.status').classList.toggle('error', error);
  document.querySelector('#status-icon').textContent = error ? '!' : '○';
  document.querySelector('#status-title').textContent = title;
  document.querySelector('#status-message').textContent = message;
}

function updateEditor() {
  lines.textContent = source.value.split('\n').map((_, i) => i + 1).join('\n');
  const before = source.value.slice(0, source.selectionStart).split('\n');
  document.querySelector('#position').textContent = `Ln ${before.length}, Col ${before.at(-1).length + 1}`;
  lines.scrollTop = source.scrollTop;
}

function changed() {
  revision++;
  updateEditor();
  setStatus('Code changed.', 'Analyze again to refresh the results.');
  tokensPanel.replaceChildren(emptyMessage('Analyze your updated code to see its tokens.'));
  treePanel.replaceChildren(emptyMessage('Analyze your updated code to see its syntax tree.'));
  document.querySelector('#token-count').textContent = '0';
}

function emptyMessage(message) {
  const container = document.createElement('div');
  container.className = 'empty';
  const text = document.createElement('p');
  text.textContent = message;
  container.append(text);
  return container;
}

function showTokens(tokens) {
  document.querySelector('#token-count').textContent = tokens.length;
  if (!tokens.length) {
    tokensPanel.replaceChildren(emptyMessage('No tokens to display.'));
    return;
  }
  const table = document.createElement('table');
  const head = table.createTHead().insertRow();
  for (const label of ['LINE', 'TOKEN', 'LEXEME']) {
    const cell = document.createElement('th');
    cell.scope = 'col';
    cell.textContent = label;
    head.append(cell);
  }
  const body = table.createTBody();
  for (const [type, value, line] of tokens) {
    const row = body.insertRow();
    for (const text of [line, type, value === '\n' ? '↵' : value]) {
      row.insertCell().textContent = text;
    }
  }
  tokensPanel.replaceChildren(table);
}

async function analyze() {
  if (analyzing) return;
  analyzing = true;
  analyzeButton.disabled = true;
  const currentRevision = revision;
  setStatus('Analyzing…', 'Reading tokens and building your syntax tree.');
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({source: source.value})
    });
    const result = await response.json();
    if (currentRevision !== revision) return;
    if (!response.ok) throw new Error(result.message || 'Analysis request failed.');
    showTokens(result.tokens);
    if (result.ok) {
      const tree = document.createElement('pre');
      tree.className = 'tree';
      tree.textContent = JSON.stringify(result.ast, null, 2);
      treePanel.replaceChildren(tree);
      setStatus('Syntax looks good.', `${result.tokens.length} tokens · ${result.ast.body.length} top-level statements · ${result.ast.functions.length} functions. Your program is ready for the next stage.`);
    } else {
      treePanel.replaceChildren(emptyMessage('Fix the syntax error and analyze again to build the tree.'));
      setStatus(`${result.error.stage === 'lexer' ? 'Lexer' : 'Parser'} error`, result.error.message, true);
    }
  } catch (error) {
    if (currentRevision === revision) {
      setStatus('Could not analyze code.', `${error.message} Make sure the Python server is running.`, true);
    }
  } finally {
    analyzing = false;
    analyzeButton.disabled = false;
  }
}

const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(tab) {
  tabs.forEach(item => {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
    document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
  });
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', event => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
    selectTab(tabs[next]);
    tabs[next].focus();
  });
});
source.addEventListener('input', changed);
source.addEventListener('click', updateEditor);
source.addEventListener('keyup', updateEditor);
source.addEventListener('scroll', () => { lines.scrollTop = source.scrollTop; });
source.addEventListener('keydown', event => {
  if (event.key === 'Tab') {
    event.preventDefault();
    source.setRangeText('    ', source.selectionStart, source.selectionEnd, 'end');
    changed();
  }
});
document.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    event.preventDefault();
    analyze();
  }
});
analyzeButton.addEventListener('click', analyze);
document.querySelector('#load').addEventListener('click', () => {
  if (source.value.trim() && !confirm('Replace the current code with this example?')) return;
  source.value = examples[document.querySelector('#example').value];
  changed();
});
document.querySelector('#open').addEventListener('click', () => document.querySelector('#file').click());
document.querySelector('#file').addEventListener('change', async event => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    if (file.size > 90000) throw new Error('Choose a file smaller than 90 KB.');
    if (source.value.trim() && !confirm('Replace the current code with this file?')) return;
    source.value = await file.text();
    changed();
  } catch (error) {
    setStatus('Could not open file.', error.message, true);
  } finally {
    event.target.value = '';
  }
});
document.querySelector('#download').addEventListener('click', () => {
  const url = URL.createObjectURL(new Blob([source.value], {type: 'text/plain;charset=utf-8'}));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'playground.lol';
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
source.value = examples.hello;
updateEditor();
