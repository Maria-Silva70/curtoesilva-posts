// Base de orçamentos · Curto e Silva
// Recebe os orçamentos do gerador (curtoesilva.com.br/orcamento-equipe),
// dá um número que nunca se repete, guarda na planilha e o PDF no Drive.

const CHAVE = 'CS-SN5F66'; // código da equipe (o mesmo digitado no gerador)
const COLS = ['Nº','Criado em','Atualizado em','Cliente','Telefone','Endereço','Serviços','Total (R$)','Situação','PDF','Feito por','Versões'];

function configurar() {
  const p = PropertiesService.getScriptProperties();
  if (!p.getProperty('SS')) {
    const pasta = DriveApp.createFolder('Orçamentos Curto e Silva');
    const ss = SpreadsheetApp.create('Base de Orçamentos · Curto e Silva');
    DriveApp.getFileById(ss.getId()).moveTo(pasta);
    const sh = ss.getSheets()[0];
    sh.setName('Orçamentos');
    sh.getRange(1, 1, 1, COLS.length).setValues([COLS]).setFontWeight('bold').setBackground('#141414').setFontColor('#FFFFFF');
    sh.setFrozenRows(1);
    sh.setColumnWidths(1, COLS.length, 130);
    sh.setColumnWidth(7, 320);
    const regra = SpreadsheetApp.newDataValidation()
      .requireValueInList(['Rascunho', 'Enviado', 'Aprovado', 'Recusado', 'Sem resposta'], true).build();
    sh.getRange('I2:I1000').setDataValidation(regra);
    sh.getRange('H2:H1000').setNumberFormat('R$ #,##0.00');
    sh.getRange('A2:A1000').setNumberFormat('@');
    sh.getRange('E2:E1000').setNumberFormat('@');
    sh.getRange('B2:C1000').setNumberFormat('dd/mm/yyyy hh:mm');
    p.setProperty('SS', ss.getId());
    p.setProperty('PASTA', pasta.getId());
  }
  Logger.log('Planilha: ' + SpreadsheetApp.openById(p.getProperty('SS')).getUrl());
}

function responder(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function doGet() { return responder({ ok: true, base: 'Curto e Silva' }); }

function doPost(e) {
  let d;
  try { d = JSON.parse(e.postData.contents); } catch (x) { return responder({ ok: false, erro: 'dados' }); }
  if (d.chave !== CHAVE) return responder({ ok: false, erro: 'chave' });
  const p = PropertiesService.getScriptProperties();
  const sh = SpreadsheetApp.openById(p.getProperty('SS')).getSheetByName('Orçamentos');

  if (d.acao === 'buscar') {
    const sem = t => String(t || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const q = sem(d.q).trim();
    const v = sh.getDataRange().getDisplayValues().slice(1).reverse();
    const achados = v.filter(r => r[0] && (!q || sem([r[0], r[3], r[4], r[5]].join(' ')).indexOf(q) >= 0))
      .slice(0, 40)
      .map(r => ({ num: r[0], data: r[1], cliente: r[3], endereco: r[5], servicos: r[6], total: r[7], situacao: r[8], pdf: (String(r[9]).match(/[-\w]{25,}/) || [''])[0], quem: r[10] }));
    return responder({ ok: true, itens: achados, total: v.filter(r => r[0]).length });
  }

  if (d.acao === 'pdf') {
    const f = DriveApp.getFileById(String(d.id || ''));
    const dentro = f.getParents().hasNext() && f.getParents().next().getId() === p.getProperty('PASTA');
    if (!dentro || f.getMimeType() !== 'application/pdf') return responder({ ok: false, erro: 'arquivo' });
    return responder({ ok: true, nome: f.getName(), b64: Utilities.base64Encode(f.getBlob().getBytes()) });
  }

  const trava = LockService.getScriptLock();
  trava.waitLock(25000);
  try {
    const agora = new Date();
    if (d.acao === 'teste') return responder({ ok: true });

    if (d.acao === 'numero') {
      const ano = agora.getFullYear();
      const k = 'ULTIMO_' + ano;
      const n = Number(p.getProperty(k) || 0) + 1;
      p.setProperty(k, String(n));
      const num = ano + '-' + ('00' + n).slice(-3);
      sh.appendRow([num, agora, agora, d.cliente || '', '', '', '', '', 'Rascunho', '', d.quem || '', 0]);
      return responder({ ok: true, num: num });
    }

    if (d.acao === 'salvar') {
      const ult = sh.getLastRow();
      const nums = ult > 1 ? sh.getRange(2, 1, ult - 1, 1).getDisplayValues().map(r => r[0]) : [];
      const i = nums.indexOf(String(d.num));
      let link = '';
      if (d.pdf) {
        const pasta = DriveApp.getFolderById(p.getProperty('PASTA'));
        const blob = Utilities.newBlob(Utilities.base64Decode(d.pdf), 'application/pdf', d.arquivo || (d.num + '.pdf'));
        link = pasta.createFile(blob).getUrl();
      }
      if (i < 0) {
        sh.appendRow([d.num, agora, agora, d.cliente, d.tel, d.endereco, d.servicos, d.total, 'Enviado', link, d.quem, 1]);
      } else {
        const r = i + 2;
        const atual = sh.getRange(r, 1, 1, COLS.length).getValues()[0];
        const situacao = (!atual[8] || atual[8] === 'Rascunho') ? 'Enviado' : atual[8];
        sh.getRange(r, 3, 1, 10).setValues([[agora, d.cliente, d.tel, d.endereco, d.servicos, d.total, situacao, link || atual[9], d.quem, Number(atual[11] || 0) + 1]]);
      }
      return responder({ ok: true, num: d.num, pdf: link });
    }
    return responder({ ok: false, erro: 'acao' });
  } finally {
    trava.releaseLock();
  }
}

// Apaga só o orçamento de teste do Claude e volta a numeração (usado na instalação)
function limparTeste() {
  const p = PropertiesService.getScriptProperties();
  const sh = SpreadsheetApp.openById(p.getProperty('SS')).getSheetByName('Orçamentos');
  const v = sh.getDataRange().getValues();
  for (let r = v.length - 1; r >= 1; r--) {
    if (v[r][3] === 'TESTE CLAUDE') {
      const id = (String(v[r][9] || '').match(/[-\w]{25,}/) || [])[0];
      if (id) DriveApp.getFileById(id).setTrashed(true);
      sh.deleteRow(r + 1);
    }
  }
  if (sh.getLastRow() <= 1) p.setProperty('ULTIMO_' + new Date().getFullYear(), '0');
  Logger.log('Linhas: ' + (sh.getLastRow() - 1) + ' · último número: ' + p.getProperty('ULTIMO_' + new Date().getFullYear()));
}
