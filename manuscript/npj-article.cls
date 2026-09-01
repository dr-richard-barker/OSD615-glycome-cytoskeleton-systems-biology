\ProvidesClass{npj-article}[2026/09/01 NPJ Article Class]
\LoadClass[twocolumn,10pt,letterpaper]{article}

\RequirePackage[utf8]{inputenc}
\RequirePackage[margin=1in]{geometry}
\RequirePackage{xcolor}
\RequirePackage{helvet}
\RequirePackage{newtxtext,newtxmath}
\RequirePackage{graphicx}
\RequirePackage[numbers,super]{natbib}
\RequirePackage{hyperref}
\RequirePackage{lineno}
\RequirePackage{booktabs}
\RequirePackage{caption}

\definecolor{npjblue}{HTML}{004D73}
\definecolor{npjorange}{HTML}{D62828}
\definecolor{linkblue}{HTML}{0056b3}

\hypersetup{colorlinks=true,linkcolor=npjblue,citecolor=npjblue,urlcolor=linkblue}

\renewcommand{\familydefault}{\rmdefault}
\newcommand{\sffont}{\fontfamily{phv}\selectfont}

\newenvironment{npjabstract}{
    \twocolumn[
    \begin{@twocolumnfalse}
    \vspace{1cm}
    \noindent\textbf{\Large Abstract}\par\vspace{0.5cm}
    \noindent
}{
    \vspace{1cm}
    \end{@twocolumnfalse}
    ]
}

\endinput
