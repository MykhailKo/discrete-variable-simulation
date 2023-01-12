from statistics import mean
from xlwt import Workbook, easyxf

COLUMNS_TITLES = ['Time',	'X Probs',	'Experiment',
                  'Theor E(X)', 'Sim E(X)',	'ε(E)', 'Theor D(X)', 'Sim D(X)', 'ε(D)', 'Theor P(3≤X≤5)',	'Sim P(3≤X≤5)',	'ε(P)']

STYLE_HEADER = easyxf(
    'font: name Calibri, color white, height 240; borders: left_color black, top_color black, right_color black, bottom_color black, left thin, top thin, right thin, bottom thin; pattern: pattern solid, fore_color light_blue; alignment: horz center')
STYLE_CONTENT = easyxf('font: name Calibri, color black, height 220; borders: left_color black, top_color black, right_color black, bottom_color black, left thin, top thin, right thin, bottom thin; alignment: horz center, vert center')
STYLE_EMPH = easyxf('font: name Calibri, color black, height 220; borders: left_color black, top_color black, right_color black, bottom_color black, left thin, top thin, right thin, bottom thin; pattern: pattern solid, fore_color light_yellow; alignment: horz center, vert center')


class ReportBuilder:
    def __init__(self):
        self.workbook = Workbook()
        self.worksheet = self.workbook.add_sheet('Statistical results')
        self.current_row = 0
        self.write_header()
        self.worksheet.col(0).width, self.worksheet.col(
            1).width, self.worksheet.col(2).width = 1700, 6100, 3000

    def write_header(self):
        for i in range(len(COLUMNS_TITLES)):
            self.worksheet.col(i).width = 4000
            self.worksheet.write(self.current_row, i,
                                 COLUMNS_TITLES[i], STYLE_HEADER)
        self.current_row += 1

    def write_experiments_section(self, experiment_records, time, probs):
        section_start_row = self.current_row
        for i in range(len(experiment_records)):
            rec = experiment_records[i]
            rec_flattened = [
                i+1, rec['ref']['exp_val'], rec['sim']['exp_val'], rec['err']['exp_val'],
                rec['ref']['dispersion'], rec['sim']['dispersion'], rec['err']['dispersion'],
                rec['ref']['seg_prob'], rec['sim']['seg_prob'], rec['err']['seg_prob']
            ]
            for i in range(2, len(COLUMNS_TITLES)):
                self.worksheet.write(self.current_row, i,
                                     rec_flattened[i-2], STYLE_CONTENT)
            self.current_row += 1
        self.worksheet.write_merge(
            section_start_row, self.current_row-1, 0, 0, time, STYLE_CONTENT)
        self.worksheet.write_merge(
            section_start_row, self.current_row-1, 1, 1, ','.join(map(str, probs)), STYLE_CONTENT)
        self.worksheet.write(self.current_row, 0, 'Average', STYLE_EMPH)
        self.worksheet.write(self.current_row, 5, round(
            mean([rec['err']['exp_val'] for rec in experiment_records]), 4), STYLE_EMPH)
        self.worksheet.write(self.current_row, 8, round(
            mean([rec['err']['dispersion'] for rec in experiment_records]), 4), STYLE_EMPH)
        self.worksheet.write(self.current_row, 11, round(
            mean([rec['err']['seg_prob'] for rec in experiment_records]), 4), STYLE_EMPH)
        self.current_row += 1

    def finish(self):
        self.workbook.save('./report.xls')
