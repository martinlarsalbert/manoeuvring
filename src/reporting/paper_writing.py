import rolldecay
import os
import matplotlib.pyplot as plt
import matplotlib
import re
import sympy as sp
import rolldecayestimators.equations
from latex_helpers.pylatex_extenders import GeneralContainer

def setup(rcParams):
    # Change to paper custom style:
    matplotlibrc_path = os.path.join(os.path.dirname(__file__),'matplotlibrc')
    #rcParams.update(matplotlib.rc_params_from_file(matplotlibrc_path))

# \label{eq:roll_decay_equation_cubic}
regexp_label = re.compile(pattern=r'\\label{eq\:([^}]+)', flags=re.MULTILINE)

# \input{equations/roll_decay_equation_himeno_linear}
regexp_input = re.compile(pattern=r'\\input{([^}]+)', flags=re.MULTILINE)

def save_fig(fig, name, full_page=False, width_cm=15):
    """
    Save a figure to the paper
    :param fig: figure handle
    :param name: figure name (without extension)
    :param full_page: default None
    :width_cm width in cm
    :return: None
    """

    fnames = [
        os.path.join(rolldecay.paper_figures_path, '%s.eps' % name),
        os.path.join(rolldecay.paper_figures_path, '%s.pdf' % name),
    ]

    fig.tight_layout()

    size = fig.get_size_inches()

    cm_to_inches = 0.393700787
    width = cm_to_inches*width_cm

    #if full_page:
    #    height = width*1.618
    #
    #else:
    #    height = width / 1.618

    #fig.set_dpi(300)
    #fig.set_size_inches(width, height)
    #plt.tight_layout()

    for fname in fnames:
        fig.savefig(fname=fname,dpi=300)

def generate_nomenclature(paper_path=None,exclude_dirs=['equations']):
    """
    Generate a nomenclature based on the equation labels in the tex files under paper_path folder
    :param paper_path: None->Default is present paper
    :return:
    """
    eq_labels=[]

    if paper_path is None:
        paper_path=rolldecay.paper_path

    file_paths = _find_tex_files(paper_path=paper_path, exclude_dirs=exclude_dirs)

    for file_path in file_paths:
        with open(file_path, mode='r') as file:
            s = file.read()

        eq_labels+=_find_eq_labels(s=s)

    input_paths = _find_inputs_in_files(file_paths)
    for file_path in input_paths:

        if not os.path.exists(file_path):
            file_path=os.path.join(paper_path,file_path)
            _,ext = os.path.splitext(file_path)
            if ext=='':
                file_path+='.tex'

        with open(file_path, mode='r') as file:
            s = file.read()


        eq_labels+=_find_eq_labels(s=s)

    equation_dict = _match_sympy_equations(eq_labels=eq_labels)
    symbols = _get_symbols(equation_dict=equation_dict)

    latex_nomenclature = _generate_latex_nomenclature(symbols=symbols)

    return latex_nomenclature

def _find_tex_files(paper_path, exclude_dirs=['equations']):

    file_paths = []
    for root, dirs, files in os.walk(paper_path, topdown=False):

        # Could this directory be excluded?
        exclude=False
        for exclude_dir in exclude_dirs:
            if exclude_dir in root:
                exclude=True
                break
        if exclude:
            continue

        for name in files:
            if os.path.splitext(name)[-1]=='.tex':
                path = os.path.join(root, name)
                file_paths.append(path)

    return file_paths

def _find_eq_labels(s:str):
    return regexp_label.findall(string=s)

def _find_inputs_in_files(file_paths:list):

    input_paths = []
    for file_path in file_paths:
        with open(file_path, mode='r') as file:
            s = file.read()

        input_paths+=_find_inputs(s=s)

    input_paths=list(set(input_paths))  # Remove possible duplicates

    return input_paths

def _find_inputs(s:str):
    return regexp_input.findall(string=s)


def _match_sympy_equations(eq_labels):
    avaliable_equation_dict = {key: value for key, value in rolldecayestimators.equations.__dict__.items() if isinstance(value, sp.Eq)}
    equation_dict = {}

    for eq_label in eq_labels:
        if eq_label in avaliable_equation_dict:
            equation_dict[eq_label] = avaliable_equation_dict[eq_label]

    return equation_dict

def _get_symbols(equation_dict:dict):

    symbols = {}
    for name,eq in equation_dict.items():
        free_symbols = {symbol.name:symbol for symbol in eq.free_symbols}
        symbols.update(free_symbols)

    return symbols

def _latex_unit(unit:str):
    latex_unit = unit.replace('**', r'^')
    #latex_unit=latex_unit.replace('*',r'\cdot ')
    latex_unit='%s'%latex_unit
    return latex_unit


def _generate_latex_nomenclature(symbols):

    """
    The method should create something like this:

    \mbox{}
    \nomenclature{$c$}{Speed of light in a vacuum inertial frame \nomunit{$m/s$}}
    \nomenclature{$h$}{Planck constant}
    \printnomenclature
    """

    content = ''
    for name,symbol in sorted(symbols.items()):
        assert isinstance(symbol,sp.Symbol)

        description = ''
        unit = ''

        if hasattr(symbol,'description'):
            description=symbol.description
            description=description[0].lower() + description[1:]
        else:
            if name == 't':
                description='time'
                unit='s'

        if hasattr(symbol, 'unit'):
            unit=_latex_unit(unit=symbol.unit)

        latex = symbol._repr_latex_()

        row = r'\nomenclature{'+latex+'}{'+description+ r'\nomunit{' + unit + '}}\n'
        content+=row

    latex_nomenclature = r"\mbox{}" + '\n' + content + '\n' + r"\printnomenclature"
    return latex_nomenclature

def save_table(file_path, tabular_tex:str, label:str, caption:str):

    tabular_tex=tabular_tex.replace('\$','$')
    tabular_tex=tabular_tex.replace(r'\textasciicircum ','^')

    latex="""
\\begin{table}[H]
    \centering
    \caption{%s}
   %s
    \label{%s}
\end{table}
    """ % (caption,tabular_tex,label)

    container = GeneralContainer()
    container.append(latex)

    container.generate_tex(file_path)
