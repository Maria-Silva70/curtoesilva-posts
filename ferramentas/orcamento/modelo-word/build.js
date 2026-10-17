const fs = require('fs');
const path = require('path');
const D = require('docx');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, BorderStyle, ImageRun, Header, Footer, VerticalAlign, ExternalHyperlink,
  TableLayoutType, HeightRule, LevelFormat
} = D;

const dir = __dirname;
const OR = 'E8601C', BK = '141414', GR = '6B6B6B', LG = 'FFF1E8', LINE = 'E3E3E3';
const FONT = 'Arial';
const W = 10466; // A4 width 11906 - margins 720*2

const none = { style: BorderStyle.NIL, size: 0, color: 'auto' };
const noB = { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };
const thin = { style: BorderStyle.SINGLE, size: 4, color: LINE };

const t = (text, o = {}) => new TextRun({ text, font: FONT, size: o.size || 19, bold: o.bold, color: o.color || BK, italics: o.it, highlight: o.hl, characterSpacing: o.sp });
// campo para preencher: amarelo
const f = (text, o = {}) => t(text, { ...o, hl: 'yellow' });
const p = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [runs], alignment: o.align, spacing: { before: o.before || 0, after: o.after ?? 60, line: o.line || 276 }, keepNext: o.keepNext, border: o.border, indent: o.indent });

function cell(children, o = {}) {
  return new TableCell({
    children: Array.isArray(children) ? children : [children],
    width: { size: o.w, type: WidthType.DXA },
    shading: o.fill ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fill } : undefined,
    margins: { top: o.mt ?? 90, bottom: o.mb ?? 90, left: o.ml ?? 140, right: o.mr ?? 140 },
    verticalAlign: o.va || VerticalAlign.CENTER,
    borders: o.borders || { top: none, bottom: none, left: none, right: none },
    columnSpan: o.span,
  });
}
const table = (widths, rows, o = {}) => new Table({ width: { size: widths.reduce((a, b) => a + b), type: WidthType.DXA }, columnWidths: widths, rows, borders: o.borders || noB, layout: TableLayoutType.FIXED });

// título de seção: número laranja + texto
function secao(num, titulo) {
  return p([t(num + '  ', { bold: true, color: OR, size: 24 }), t(titulo.toUpperCase(), { bold: true, size: 22, sp: 20 })],
    { before: 260, after: 120, keepNext: true, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: OR, space: 4 } } });
}

const img = (file, w, h) => new ImageRun({ type: 'png', data: fs.readFileSync(path.join(dir, file)), transformation: { width: w, height: h } });

// ---------- CABEÇALHO ----------
const header = new Header({
  children: [
    table([1500, 5466, 3500], [new TableRow({
      children: [
        cell(new Paragraph({ children: [img('logo.png', 66, 66)], spacing: { before: 0, after: 0 } }), { w: 1500, fill: BK, ml: 260, mt: 120, mb: 120 }),
        cell([
          p(t('CURTO E SILVA', { bold: true, size: 34, color: 'FFFFFF', sp: 30 }), { after: 0 }),
          p(t('Reformas, construção e manutenção · BH, Contagem e Nova Lima', { size: 16, color: 'D0D0D0' }), { after: 0 }),
        ], { w: 5466, fill: BK }),
        cell([
          p(t('ORÇAMENTO', { bold: true, size: 26, color: OR, sp: 40 }), { align: AlignmentType.RIGHT, after: 0 }),
          p([t('Nº ', { size: 18, color: 'FFFFFF' }), f('2026-000', { size: 18, color: BK, bold: true })], { align: AlignmentType.RIGHT, after: 0 }),
        ], { w: 3500, fill: BK, mr: 260 }),
      ],
    })]),
    p(t(''), { after: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 24, color: OR, space: 0 } } }),
  ],
});

// ---------- RODAPÉ ----------
const footer = new Footer({
  children: [
    p([
      new ExternalHyperlink({ link: 'https://wa.me/5531999846776', children: [t('WhatsApp (31) 99984-6776', { size: 16, bold: true, color: BK })] }),
      t('   ·   atendimento@curtoesilva.com.br   ·   @curtoesilva   ·   curtoesilva.com.br', { size: 16, color: GR }),
    ], { align: AlignmentType.CENTER, after: 20, border: { top: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 6 } } }),
    p(t('A nova geração que honra o velho compromisso.', { size: 16, it: true, color: OR, bold: true }), { align: AlignmentType.CENTER, after: 0 }),
  ],
});

const body = [];

// Título e saudação
body.push(p(t('Orçamento de manutenção', { bold: true, size: 36 }), { before: 120, after: 40 }));
body.push(p([t('Olá, ', { color: GR }), f('[Nome do cliente]', { color: GR }), t('! Obrigado por chamar a Curto e Silva. Este orçamento foi feito depois da visita técnica, com tudo o que vimos no local.', { color: GR })], { after: 200 }));

// Ficha cliente / empresa
const lab = (s) => t(s, { size: 15, color: GR, bold: true, sp: 10 });
const ficha = (rows) => rows.map(([l, v]) => p([lab(l.toUpperCase() + '  '), ...(Array.isArray(v) ? v : [v])], { after: 50 }));
body.push(table([5233, 5233], [new TableRow({
  children: [
    cell([p(t('PARA', { bold: true, color: OR, size: 17, sp: 30 }), { after: 80 }), ...ficha([
      ['Cliente', f('[Nome do cliente]')],
      ['Endereço da obra', f('[Rua, número – bairro, cidade]')],
      ['Telefone', f('[(31) 9____-____]')],
      ['Data da visita', f('[__/__/2026]')],
    ])], { w: 5233, fill: 'F6F6F6', va: VerticalAlign.TOP, ml: 220, mt: 160, mb: 160 }),
    cell([p(t('DE', { bold: true, color: OR, size: 17, sp: 30 }), { after: 80 }), ...ficha([
      ['Empresa', t('Curto e Silva – Reformas e Construção')],
      ['CNPJ', t('30.569.236/0001-04')],
      ['Responsável', t('Allan Curto')],
      ['Data do orçamento', f('[__/__/2026]')],
    ])], { w: 5233, fill: 'F6F6F6', va: VerticalAlign.TOP, ml: 220, mt: 160, mb: 160, borders: { left: { style: BorderStyle.SINGLE, size: 12, color: 'FFFFFF' }, top: none, bottom: none, right: none } }),
  ],
})]));

// 1. O que encontramos
body.push(secao('01', 'O que encontramos na visita'));
body.push(table([W], [new TableRow({
  children: [cell([
    p(f('[Explique em 2 ou 3 frases simples o problema e a causa. Ex.: "A água da chuva está entrando pelo buraco da antena e pela calha, que está solta em cima da mureta. Isso causa a infiltração na parede do quarto."]', { it: true }), { after: 0 }),
  ], { w: W, fill: LG, ml: 240, mr: 240, mt: 160, mb: 160, borders: { left: { style: BorderStyle.SINGLE, size: 24, color: OR }, top: none, bottom: none, right: none } })],
})]));

// 2. Serviços (mão de obra) — tabela por etapa
body.push(secao('02', 'O que vamos fazer (mão de obra)'));
const servHead = new TableRow({
  tableHeader: true,
  children: [
    cell(p(t('ITEM', { bold: true, color: 'FFFFFF', size: 16 })), { w: 900, fill: BK }),
    cell(p(t('SERVIÇO', { bold: true, color: 'FFFFFF', size: 16 })), { w: 7366, fill: BK }),
    cell(p(t('VALOR (opcional)', { bold: true, color: 'FFFFFF', size: 16 }), { align: AlignmentType.RIGHT }), { w: 2200, fill: BK }),
  ],
});
const servicos = [
  'Tampar o buraco da antena com manta aluminizada',
  'Alinhar as telhas próximas à calha',
  'Aplicar argamassa AC3 em cima da mureta para fixar a calha',
  'Comprar e instalar rufo em "U" no topo da mureta',
  'Fixar o rufo antigo desalinhado e vedar com PU ou manta aluminizada',
  'Aplicar manta líquida na parte interna da calha',
];
const servRows = servicos.map((s, i) => new TableRow({
  cantSplit: true,
  children: [
    cell(p(t(`1.${i + 1}`, { bold: true, color: OR })), { w: 900, fill: i % 2 ? 'FFFFFF' : 'FAFAFA', borders: { bottom: thin, top: none, left: none, right: none } }),
    cell(p(f(s)), { w: 7366, fill: i % 2 ? 'FFFFFF' : 'FAFAFA', borders: { bottom: thin, top: none, left: none, right: none } }),
    cell(p(f('R$ ___'), { align: AlignmentType.RIGHT }), { w: 2200, fill: i % 2 ? 'FFFFFF' : 'FAFAFA', borders: { bottom: thin, top: none, left: none, right: none } }),
  ],
}));
body.push(table([900, 7366, 2200], [servHead, ...servRows]));
body.push(p(t('Para mais itens: clique na última linha da tabela e aperte Tab no final dela. Se não quiser mostrar valor por item, apague a coluna "Valor".', { size: 15, it: true, color: GR }), { before: 60, after: 0 }));

// 3. Materiais
body.push(secao('03', 'Materiais inclusos'));
const mats = ['Manta aluminizada', 'Maçarico', 'Argamassa AC3', 'Rufos', 'PU (selante)', 'Manta líquida'];
const half = Math.ceil(mats.length / 2);
const matCol = (arr, start) => arr.map((m, i) => p([t('✓  ', { bold: true, color: OR, size: 20 }), t(`2.${start + i} – `, { color: GR }), f(m)], { after: 70 }));
body.push(table([5233, 5233], [new TableRow({
  children: [
    cell(matCol(mats.slice(0, half), 1), { w: 5233, va: VerticalAlign.TOP, ml: 60 }),
    cell(matCol(mats.slice(half), half + 1), { w: 5233, va: VerticalAlign.TOP, ml: 60 }),
  ],
})]));
body.push(p(t('Todo o material necessário já está no valor. Você não precisa comprar nada.', { size: 17, color: GR, it: true }), { before: 40, after: 0 }));

// 4. Investimento
body.push(secao('04', 'Investimento'));
body.push(table([6466, 4000], [new TableRow({
  cantSplit: true,
  children: [
    cell([
      p(t('VALOR TOTAL', { bold: true, color: OR, size: 17, sp: 40 }), { after: 40 }),
      p(t('Mão de obra + todo o material para a execução do serviço', { color: 'FFFFFF', size: 18 }), { after: 40 }),
      p(t('([valor por extenso] reais)', { size: 17, it: true, color: 'BBBBBB' }), { after: 0 }),
    ], { w: 6466, fill: BK, ml: 280, mt: 220, mb: 220 }),
    cell(p(t('R$ 0.000,00', { bold: true, size: 44, color: OR }), { align: AlignmentType.RIGHT }), { w: 4000, fill: BK, mr: 280 }),
  ],
})]));

// Condições em cartões
const card = (titulo, linhas, w) => cell([
  p(t(titulo.toUpperCase(), { bold: true, size: 15, color: OR, sp: 20 }), { after: 60 }),
  ...linhas.map(l => p(Array.isArray(l) ? l : [l], { after: 30 })),
], { w, fill: 'F6F6F6', va: VerticalAlign.TOP, ml: 180, mt: 150, mb: 150, borders: { top: none, bottom: none, left: none, right: { style: BorderStyle.SINGLE, size: 24, color: 'FFFFFF' } } });
body.push(p(t(''), { after: 120 }));
body.push(table([2617, 2617, 2616, 2616], [new TableRow({
  cantSplit: true,
  children: [
    card('Pagamento', [t('50% de sinal'), t('50% na conclusão')], 2617),
    card('Prazo', [f('[01 a 02 dias]'), t('de execução', { color: GR, size: 17 })], 2617),
    card('Início', [f('[a combinar]'), t('após o sinal', { color: GR, size: 17 })], 2616),
    card('Validade', [[t('Até '), f('[__/__/2026]')]], 2616),
  ],
})]));
body.push(p([t('Garantia do serviço: ', { bold: true }), f('[preencher com o Allan, ex.: __ meses para a mão de obra]')], { before: 140, after: 40 }));
body.push(p([t('Não está incluso: ', { bold: true }), f('[serviços que não estão na lista acima, ex.: pintura da parede interna]')], { after: 0 }));

// 5. Como trabalhamos
body.push(secao('05', 'Como trabalhamos'));
const passos = [
  ['1', 'Visita', 'Avaliamos o local e explicamos a causa. Sem custo.'],
  ['2', 'Orçamento', 'Por escrito, separado por etapa, sem surpresa.'],
  ['3', 'Execução', 'Equipe própria, com acompanhamento até o fim.'],
  ['4', 'Entrega', 'Limpeza do local e conferência junto com você.'],
];
body.push(table([2617, 2617, 2616, 2616], [new TableRow({
  cantSplit: true,
  children: passos.map(([n, ti, tx], i) => cell([
    p([t(n, { bold: true, size: 30, color: OR }), t('  ' + ti.toUpperCase(), { bold: true, size: 17, sp: 20 })], { after: 40 }),
    p(t(tx, { size: 16, color: GR }), { after: 0 }),
  ], { w: i < 3 ? 2617 : 2616, va: VerticalAlign.TOP, ml: 120, mr: 160, borders: { top: { style: BorderStyle.SINGLE, size: 18, color: i === 0 ? OR : BK }, bottom: none, left: none, right: none } })),
})]));

// 6. Pagamento + aceite
body.push(secao('06', 'Dados para pagamento e aceite'));
body.push(table([4200, 6266], [new TableRow({
  cantSplit: true,
  children: [
    cell([
      p(t('PIX (CNPJ)', { bold: true, size: 15, color: OR, sp: 20 }), { after: 20 }),
      p(t('30.569.236/0001-04', { bold: true, size: 24 }), { after: 100 }),
      p(t('Banco Bradesco', { size: 17 }), { after: 10 }),
      p(t('Agência 2465 · Conta corrente 72572-2', { size: 17 }), { after: 10 }),
      p(t('Curto e Silva – Reformas e Construção', { size: 17, color: GR }), { after: 0 }),
    ], { w: 4200, fill: LG, va: VerticalAlign.TOP, ml: 220, mt: 180, mb: 180 }),
    cell([
      p(t('De acordo com este orçamento:', { bold: true, size: 18 }), { after: 380 }),
      p(t(''), { after: 30, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BK, space: 1 } } }),
      p([t('Cliente  ', { size: 16, color: GR }), f('[Nome do cliente]', { size: 16 }), t('        Data ____/____/______', { size: 16, color: GR })], { after: 300 }),
      p(t(''), { after: 30, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BK, space: 1 } } }),
      p(t('Allan Curto · Curto e Silva', { size: 16, color: GR }), { after: 0 }),
    ], { w: 6266, va: VerticalAlign.TOP, ml: 360, mt: 180 }),
  ],
})]));
body.push(p(t('Também vale o "de acordo" pelo WhatsApp: é só responder a mensagem com o orçamento.', { size: 15, it: true, color: GR }), { before: 80, after: 0 }));

const doc = new Document({
  creator: 'Curto e Silva',
  title: 'Modelo de orçamento – Curto e Silva',
  styles: { default: { document: { run: { font: FONT, size: 19 } } } },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 2250, bottom: 1100, left: 720, right: 720, header: 360, footer: 360 } } },
    headers: { default: header },
    footers: { default: footer },
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(path.join(dir, 'Modelo-Orcamento-Curto-e-Silva.docx'), b); console.log('ok'); });
