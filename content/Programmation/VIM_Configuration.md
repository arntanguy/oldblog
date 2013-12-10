Title: VIM : My configuration 
Date: 2009-12-23
Tags: VIM 
Summary: Configuring VIM correctly can make it a hugely efficient editor. Here you'll find my personnal configuration files that can be use for developping in many languages, mainly C++ though.


Tant qu’à m’être fait un vim qui me convient à peu près, je me suis dit que ça
pourrait être bien de partager ça. J’utilise un gestionnaire de version (git)
pour suivre l’évolution de ma configuration, le dépôt contenant le tout est
disponible sur [github](http://github.com/geenux/vim_config/).

Actuellement ma configuration permet :

* De programmer en c++ : Alternate (:A) pour passer des .cpp aux .h, Surround pour gérer les parenthèses, matchit pour étendre la commande "%" (permettant de passer de la parenthèse ouvrante à la fermante) à plus d’éléments (balises xml…), NerdCommenter pour gérer les commentaires, DoxygenToolKit pour gérer la documentation. Et le plugin le plus important : OmniCppComplete qui permet de compléter le code plus intelligemment que Ctrl+N (notemment en utilisant les fichiers tags, que j’ai réalisé pour Qt et boost sur mon ordi).

* De faire de latex : la latex-suite est installée.

* Il y a d’autres plugins intéressant, comme Arpeggio par exemple. Arpeggio permet d’utiliser des raccourcis en pressant simultanément plusieurs touches.
Par exemple, en ajoutant la ligne suivante dans le .vimrc
call arpeggio#map('i', '', 0, 'jk', '')
Ça créé un raccourcis en mode insertion, de sorte que "jk" pressés simultanément sortent du mode insertion, et que "j" et "k" pressés séparément aient toujours le même effet.

Si vous décidez d’utiliser ma configuration, téléchargez là à l’adresse indiquée plus haut, puis placez le contenu du dossier dans ~/.vim. Ensuite, déplacez le vimrc dans ~/.vimrc et gvimrc dans ~/.gvimrc.

J’ai rédigé un mini aide mémoire pour moi, faites dans vim 

    ::vim
        :h arnaud


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    *arnaud.txt*	Arnaud Vim Config          2009-06-21
    
    Author:  TANGUY Arnaud <arn.tanguy@gmail.com>
    Copyright: © Copyright 2009 TANGUY Arnaud. All Rights Reserved. Licence GNU
    GPL v2 or later (at your option)
    
    ==============================================================================
    1. Contents			*arnaud* *arnaud-contents* {{{1
    
    	1. Contents.................................: |arnaud-contents|
    	2. Key-mappings.............................: |a-keys|
        3. Plugins..................................: |a-plugins|
    	     OmniCppComplete........................: |a-omnicppcomplete|
    	     Project................................: |a-project|
    	     SearchInRuntime........................: |a-searchinruntime|
    	     Surround...............................: |a-surround|
    	     Alternate..............................: |a-alternate|
             ManPageView............................: |a-manpageview|
             Matchit................................: |a-matchit|
             NERD_Commenter.........................: |a-nerdcommenter|
             PhpDocumentor..........................: |a-phpdocumentor|
             DoxygenToolkit.........................: |a-doxygen|
             Markdown...............................: |a-markdown|
             Indent Guides..........................: |a-indent-guides|
    
    ==============================================================================
    2. Key mappings                         *a-key* *a-keys* {{{1
           ,cd      cd to the directory of the current view
           <F6>     SearchInVar and open in the current view
           <F7>     SearchInVar and open in a new tab
           <F1>     Project open the project window
           <F2>     Ctags rebuild. In insert and normal modes
           <F9>     Build the file or project. It's a ftplugin, so it may not be
                    mapped in every mode
           <C-D>    Generate doc for a function (or class). It is used by
                   ftplugins, at least the php one.
    
    3. Plugins                  *a-plugins* *a-plugin* {{{1
    
        OMNICPPCOMPLETE                             *a-omnicppcomplete* {{{2
        Omnicppcomplete is a completition plugin. It completes the code, maily
        the c++ ones.
        It is based on ctags, so it requires a tags file, which can be created
        with:
        ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .
        Then, the autocompletition is with <C-x><C-o> (automatically called in
        my config)
        See |omnicppcomplete.txt|
    
        PROJECT                                   *a-project* *a-projects* {{{2
        A project managment plugin. It allows to remember the project
        structures, and re-open it easily.
        - \c creates a new project
        - :w saves it
        - SPACE grow/reduce the project window
        See |project.cpp|
    
        SEARCHINRUNTIME                     *a-searchinruntime* *a-SIR* {{{2
        Search a file name or a variable in the PATH. It provides an easy way
        to load files.
        See |searchInRuntime.txt|
    
        SURROUND                             *a-surround* {{{2
        It is a plugin to surround text with caracters like {,(, "...
        - cs({  : replace (...) with { ... }
        cs(}  : replace (...) with {...} (without spaces)
        cs{<q> : replace {...} with <q>...</q>
        - ds{ : delete {}
        - ys[text element]{ : surround text element with {}
        Example : "_Hello dear friends"
        ys2w[ will give you "[ Hello dear ] friends"
        - Visual selection surrounding:
        press V or v, and then select text. Press S and type your
        surrounding character (it can be html tags).
        See |surround.txt|
    
        ALTERNATE                               *a-alternate* {{{2
        Switch between .h and .cpp (.hpp/.cpp .h/.c and so on).
    
        MANPAGEVIEW                             *a-manpageview* {{{2
        View php man pages. It requires links to work.
        Call it with K as for unixes man pages
    
        MATCHIT                                 *a-matchit* {{{2
        It allows you to configure % to match more than just
        single characters.  You can match words and even regular
        expressions.
        Also, matching treats strings and comments (as recognized by the
        syntax highlighting mechanism) intelligently.
        The default ftplugins include settings for several languages:
        Ada, ASP with VBS, Csh, DTD, Essbase, Fortran, HTML, JSP
        (same as HTML), LaTeX, Lua, Pascal, SGML, Shell, Tcsh, Vim, XML.
        (I no longer keep track, so there may be others.)
        The documentation (included in the zip file) explains how to configure
        the script for a new language and how to modify the defaults.
        See |matchit.txt|
    
        NERDCOMMENTER                      *a-nerd*  *a-nerdcommenter* {{{2
        Nerd commenter allow to comment code according to the file type.
        The most useful mappings are:
    
        ,cc |NERDComComment|
        Comments out the current line or text selected in visual mode.
        ,cy is the same, but yank before commenting
    
        ,cl OR ,cr OR ,cb |NERDComAlignedComment|
        Same as |NERDComComment| except that the delimiters are aligned down the
        left side (,cl), the right side (,cr) or both sides
        (,cb).
    
        ,cI |NERDComPrependComment| ,cA |NERDComAppendComment|
        Comment before/after the current line. Adds comment delimiters to the end of line and goes
        into insert mode  between them.
    
        ,c<space> |NERDComToggleComment|
        Toggles the comment state of the selected line(s). If the topmost selected
        line is commented, all selected lines are uncommented and vice versa.
    
        ,cu |NERDComUncommentLine|
        Uncomments the selected line(s).
    
        ,cm |NERDComMinimalComment|
        Comments the given lines using only one set of multipart delimiters if
        possible.
    
        ,ci |NERDComInvertComment|
        Toggles the comment state of the selected line(s) individually. Each
        selected
        line that is commented is uncommented and vice versa.
    
        ,cs |NERDComSexyComment|
        Comments out the selected lines ``sexily''. Useful for doc, headers...
    
        ,ca |NERDComAltDelim|
        /*Switches to the alternative set of delimiters.*/
    
        See |NERDCommenter|
    
        PHPDOCUMENTOR                                *a-phpdocumentor* *a-phpd* {{{2
        PhpDocumentor is a plugin for generating phpDocumentor documentation
        blocs.
        In my configuration, it is called with <C-P>, in every mode.
    
        DOXYGEN                                                 *a-doxygen* {{{2
        It is a plugin for autocreatin doxygen commenting blocs.
        Move on a function declaration, and :Dox or <C-P>
        See http://www.vim.org/scripts/script.php?script_id=987 for more details
        and configuration variables
    
        MARKDOWN                                     *a-markdown* {{{2
        Mappings:
        the following work on normal and visual modes:
        - ]]: go to next header
        - [[: go to previous header
        - ][: go to next sibling header if any
        - []: go to previous sibling header if any
        - ]c: go to Current header
        - ]u: go to parent header (Up)
    
        INDENT GUIDES                               *a-indent-guides* {{{2
        Activate with <Leader>ig   (,ig)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
