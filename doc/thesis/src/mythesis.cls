% mythesis.cls: LaTeX2e class for writing thesis
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mythesis}[2014/06/01 My Custom Thesis class]

\LoadClassWithOptions{report}
\RequirePackage[hmargin={1in,1in},vmargin={1in,1in}]{geometry}
\RequirePackage{setspace}
\usepackage[utf8]{inputenc}

\newcommand{\thesistitle}[1]{\newcommand\Thesistitle{#1}}
\newcommand{\degreename}[1]{\newcommand\Degreename{#1}}
\newcommand{\degreefield}[1]{\newcommand\Degreefield{#1}}
\newcommand{\authorname}[1]{\newcommand\Authorname{#1}}
\newcommand{\degreeyear}[1]{\newcommand\Degreeyear{#1}}
\newcommand{\committeechair}[1]{\newcommand\Committeechair{#1}}
\newcommand{\othercommitteemembers}[1]{\newcommand\Othercommitteemembers{#1}}
\newcommand{\copyrightdeclaration}[1]{\newcommand\Copyrightdeclaration{#1}}
\newcommand{\prepublishedcopyrightdeclaration}[1]{\newcommand\Prepublishedcopyrightdeclaration{#1}}
\newcommand{\dedications}[1]{\newcommand\Dedications{#1}}
\newcommand{\acknowledgments}[1]{\newcommand\Acknowledgments{#1}}
\newcommand{\curriculumvitae}[1]{\newcommand\Curriculumvitae{#1}}
\newcommand{\thesisabstract}[1]{\newcommand\Thesisbstract{#1}}

\newcommand{\thesistitlepage}
{
	\vspace*{0.5in}
	\thispagestyle{empty}
	\singlespacing
	\begin{center}
		UNIVERSITÉ DE BOURGOGNE, \\
		Dijon, \\
		\vspace{0.4in}
		\Thesistitle \\
		\vspace{0.15in}
		MÉMOIRE \\
		\vspace{0.4in}
		\MakeUppercase\Degreename \\
		\vspace{0.15in}
		par \\
		\vspace{0.4in}
		\Authorname \\
	\end{center}
	\vspace{1in}
	\begin{flushright}
		Tuteurs: \\
		\Committeechair \\
		\Othercommitteemembers \\
	\end{flushright}
	\vfill
	\begin{center}
		\Degreeyear
	\end{center}
	\clearpage
}

\newcommand{\copyrightpage}
{
	\thispagestyle{empty}
	\rule{0in}{0in}
	\protect\vfill
	\begin{center}
		\Copyrightdeclaration
	\end{center}
	\clearpage
}

\newcommand{\prepublishedcopyrightpage}
{
	\thispagestyle{empty}
	\rule{0in}{0in}
	\protect\vfill
	\begin{center}
		\Prepublishedcopyrightdeclaration
	\end{center}
	\clearpage
}

\newcommand{\signaturepage}
{
	\vspace*{1in}
	\begin{center}
		The dissertation of \Authorname \\
		is approved and is acceptable in quality and form for \\
		publication on microfilm and in digital formats: \\
	\end{center}
	\vspace{3in}
	\begin{flushright}
	\rule{3in}{0.01in} \\
	\vspace{0.4in}
	\rule{3in}{0.01in} \\
	\vspace{0.4in}
	\rule{3in}{0.01in} \\
	Committee Chair
	\end{flushright}
	\vspace{.75in}
	\begin{center}
	University of California, Irvine \\
	\Degreeyear
	\end{center}
	\clearpage
}

\newcommand{\dedicationpage}
{
	\begin{center}
		\textbf{\Large DEDICATION} \\
		\vspace{0.4in}
		\Dedications
	\end{center}
	\clearpage
}

\newcommand{\acknowledgmentspage}
{
	\begin{center}
		\textbf{\Large REMERCIEMENTS}
	\end{center}
	\parskip 12pt
	\parindent 0pt
	\Acknowledgments
	\clearpage
}

\newcommand{\curriculumvitaepage}
{
	\begin{center}
		\textbf{\Large CURRICULUM VITAE} \\
		\vspace{0.4in}
		\textbf{\large{\Authorname}}
	\end{center}
	\Curriculumvitae
	\clearpage
}

\newcommand{\abstractpage}
{
	\begin{center}
		{\bf\Large RÉSUMÉ} \\
		\vspace{0.2in}
		\Thesistitle \\
		\vspace{0.2in}
		Par \\
		\vspace{0.2in}
		\Authorname \\
		\vspace{0.2in}
		\Degreename\ in \Degreefield \\
		\vspace{0.2in}
		Unversité de Bourgogne, Dijon, \Degreeyear \\
		\vspace{0.2in}
		\Committeechair \\
	\end{center}
	\vspace{0.2in}
	%\doublespacing
	\onehalfspacing
	\Thesisbstract
	\clearpage
}

\renewcommand{\contentsname}{\protect\centering\protect\Large TABLE DES MATIÈRES}
\renewcommand{\listfigurename}{\protect\centering\protect\Large LISTE DES FIGURES}
\renewcommand{\listtablename}{\protect\centering\protect\Large LISTE DES TABLES}

% Add "Page" as column title to Table of Contents, List of Figures,
% List of Tables, and List of Algorithms
\addtocontents{toc}{\protect\raggedleft Page\\}
\addtocontents{lof}{\protect\raggedleft Page\\}
\addtocontents{lot}{\protect\raggedleft Page\\}
\addtocontents{loa}{\protect\raggedleft Page\\}

\newcommand{\preliminarypages}
{
	\pagenumbering{gobble}% Remove page numbers (and reset to 1), see http://tex.stackexchange.com/questions/54333/no-page-numbering
	\clearpage
	\thispagestyle{empty}
	\thesistitlepage
	\clearpage
	\pagenumbering{roman}
        \ifx\Prepublishedcopyrightdeclaration\undefined
	  \copyrightpage
	\else
	  \prepublishedcopyrightpage
        \fi
	\setcounter{page}{2}
	%\signaturepage  %% not for electronic submission
        \ifx\Dedications\undefined
	\else
	  \dedicationpage
	\fi
	\tableofcontents
	\clearpage
	\phantomsection
	\addcontentsline{toc}{chapter}{LISTE DES FIGURES}
	\listoffigures
	\clearpage
	\phantomsection
	\addcontentsline{toc}{chapter}{LISTE DES TABLES}
	\listoftables
	\ifx\listalgorithmname\undefined  % for algorithm package
	\else
	  \clearpage
	  \phantomsection
	  \addcontentsline{toc}{chapter}{LISTE DES ALGORITHMES}
	  \listofalgorithms
	\fi
	\clearpage
	\phantomsection
	\addcontentsline{toc}{chapter}{REMERCIEMENTS}
	\acknowledgmentspage
	\clearpage
	\phantomsection
	%\addcontentsline{toc}{chapter}{CURRICULUM VITAE}
	%\curriculumvitaepage
	%\clearpage
	%\phantomsection
	\addcontentsline{toc}{chapter}{RÉSUMÉ}
	\abstractpage
	\clearpage
	\setcounter{page}{1}
	\pagenumbering{arabic}
}

% Reverted back to standard latex appendix, since numbering of
% figures/tables was broken with custom command.
%\renewcommand{\appendix}
\newcommand{\myappendix}
{
	\par
	\setcounter{section}{0}
	\setcounter{figure}{0}
	\setcounter{table}{0}
	\setcounter{equation}{0}
	\gdef\thechapter{\@Alph\c@section}
	\gdef\thesection{\@Alph\c@section}
	\chapter*{Appendices}
	\addcontentsline{toc}{chapter}{Appendices}
}

% Redefine the bibliography to make it single-spaced.
\renewcommand{\bibliography}[1]{%
  \if@filesw
    \immediate\write\@auxout{\string\bibdata{#1}}%
  \fi
  % Make sure the table of contents has an entry for the bibliography
  \addcontentsline{toc}{chapter}{Bibliographie}
  \begin{singlespacing}
  \@input@{\jobname.bbl}
  \end{singlespacing}
}
