## English/Chinese Resume Latex Project

This repository contains the tex documents for my resume, in both English and
Chinese language. Compiled PDFs are available from
[GitHub Releases](https://github.com/yangrq1018/resume-en-tex/releases)
and are not tracked in Git. You may freely download the source file for
modification, as template
for your own resume, or whatever you like, as long as you adhere to the LICENSE
provided.

If you are hiring managers and would like to contact me, you are also welcomed
to download the PDFs for the contact information.

I kindly ask everyone not to abuse the contact information in the resume for spam
purpose.

## How to Compile
If you are interested and would like to use the project as a template, here is
how to compile:

Install TeX Live (including `latexmk`, XeLaTeX, the extra LaTeX packages and
fonts) and the **Noto Serif CJK SC** system font. On Ubuntu:

```sh
sudo apt-get install latexmk texlive-xetex texlive-latex-extra texlive-fonts-extra \
  texlive-lang-chinese texlive-fonts-recommended fonts-font-awesome fonts-noto-cjk
```

Compile the English version with pdfLaTeX and the Chinese version with XeLaTeX:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -outdir=build main-en.tex
latexmk -norc -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main-cn.tex
```

The PDFs are written to `build/`. `-norc` skips the local preview settings in
`.latexmkrc` for a noninteractive build.

## Releases

Push a version tag in the form `vMAJOR.MINOR.PATCH` to compile both resumes and
publish `main-cn.pdf` and `main-en.pdf` as GitHub Release assets:

```sh
git tag v1.0.0
git push origin v1.0.0
```

The release workflow uses the repository's built-in `GITHUB_TOKEN`; no additional
secrets are required.

To release an existing tag after fixing a workflow failure, run the workflow
manually from the Actions tab and supply that tag as the `tag` input.
