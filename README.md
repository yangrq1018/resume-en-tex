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
  texlive-lang-chinese texlive-fonts-recommended fonts-font-awesome fonts-noto-core fonts-noto-cjk
```

Compile the English version with pdfLaTeX and the Chinese version with XeLaTeX:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -outdir=build main-en.tex
latexmk -norc -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main-cn.tex
```

The PDFs are written to `build/`. `-norc` skips the local preview settings in
`.latexmkrc` for a noninteractive build.

### Public copies

The public versions mask the telephone number and email address with solid bars
while preserving the layout. The `public` option suppresses the actual text and
the `tel:`/`mailto:` link targets before PDF generation, so the contact fields
cannot be recovered by selecting text or inspecting links.

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -outdir=build main-en-public.tex
latexmk -norc -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main-cn-public.tex
python3 scripts/check_public_pdfs.py build
```

The verification script needs `pypdf` (`python3-pypdf` on Ubuntu). Compile the two
original versions too: the check derives the contact fields from their links,
then verifies that the public copies have no email address or telephone number
in extracted text, PDF metadata or hyperlinks. A failed check blocks the Release.

## Releases

Push a version tag in the form `vMAJOR.MINOR.PATCH` to compile both resumes and
publish four GitHub Release assets:

- `main-cn.pdf` and `main-en.pdf`: original versions with contact information.
- `main-cn-public.pdf` and `main-en-public.pdf`: masked versions for public links.

The blog links to the latest public copies, so future Releases update the
downloads without copying PDFs into the blog repository:

- [Chinese public resume](https://github.com/yangrq1018/resume-en-tex/releases/latest/download/main-cn-public.pdf)
- [English public resume](https://github.com/yangrq1018/resume-en-tex/releases/latest/download/main-en-public.pdf)

```sh
git tag v1.0.0
git push origin v1.0.0
```

The release workflow uses the repository's built-in `GITHUB_TOKEN`; no additional
secrets are required.

To release an existing tag after fixing a workflow failure, run the workflow
manually from the Actions tab and supply that tag as the `tag` input.
