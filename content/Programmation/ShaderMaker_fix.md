Title: ShaderMaker: Fix bug with geometry shaders!
Date: 2013-02-03 
Tags: programmation, shadermaker, bugfix, glsl, shaders, shader editor 
Summary: When using a video card without support for goemetry shaders,
ShaderMaker's text editor crashed. Indeed, the code tries to load a geometric
shader while this isn't possible. This article provides the necessary source
code to fix this issue. 

Hi!

I’ve just tried ShaderMaker, which seemed like a great shader editor, and one of the only existing ones that is truly cross-plateform.

However, I’m still an unlucky student stuck with an integrated intel chipset, which obviously doesn’t support geometry shaders. Unfortunaly, when I tried editing a fragment shader  I bumped into a nice Segmentation fault!

I looked it up online, and the only information I could find was that ShaderMaker crashed whenever geometry shader weren’t supported by the graphics card.

Strangely enough, I couldn’t find any patch, despite the number of people complaining about it… So I decided to get my hands dirty, after all, I’m programming a physic engine and a bunch of shaders at the moment, so how hard could it be to fix a segmentation fault?

Not hard at all! The bug is a mere problem of indices, that causes the program to look for a non-existing text editor. That’s all.

Since I didn’t really have the time to delve into the code, I merely hacked the incriminated index back into behaving itself. It should work for everybody, even lucky possessors of geometry shaders enabled cards (even though they don’t need this fix).

So here goes the magick:

Download the patched version of the sources from <http://dl.free.fr/jRYRjmwEb>

And then build it using the usual method:

    ::bash
        qmake -unix ShaderMaker.pro
        make

That’s it, you’re all set and it should work.

Just in case, I’m also posting the diff file here

    ::diff
        diff --git a/src/editwindow.cpp b/src/editwindow.cpp
        index 703b95a..1da7461 100644
        --- a/src/editwindow.cpp
        +++ b/src/editwindow.cpp
        @@ -320,7 +320,7 @@ createMenus
        */
        void CBaseEditWindow::createMenus( IShader* )
        {
        - // files
        + // files
        m_menuFile = menuBar()-&gt;addMenu( tr( "&amp;File" ) );
        m_menuFile-&gt;addAction( m_actNew );
        m_menuFile-&gt;addAction( m_actOpen );
        @@ -449,7 +449,7 @@ void CSdiEditWindow::uploadShaderSource( IShader* shader )
        {
        if( m_attachToShader )
        {
        - shader-&gt;setShaderSource( m_document-&gt;shaderType(),
        + shader-&gt;setShaderSource( m_document-&gt;shaderType(),
        m_document-&gt;document()-&gt;toPlainText() );
        }
        else // disabled by the user
        @@ -766,7 +766,6 @@ void CMdiEditWindow::createMenus( IShader* shader )
        m_menuView-&gt;addAction( m_actToSDI );
        }
         
        -
        /*
        ========================
        createTabs
        @@ -777,6 +776,8 @@ void CMdiEditWindow::createTabs( IShader* shader )
        m_tabs = new QTabWidget();
         
        // add tabs
        + qDebug() &lt;&lt; "Creating " &lt;&lt; IShader::MAX_SHADER_TYPES &lt;&lt; " editors\n" ; + m_geometryShaderAvailable = shader-&gt;isShaderTypeAvailable(IShader::TYPE_GEOMETRY);
        for( int i = 0 ; i &lt; IShader::MAX_SHADER_TYPES ; i++ ) { m_editors[ i ] = NULL; @@ -805,14 +806,26 @@ void CMdiEditWindow::createTabs( IShader* shader ) connect( m_signalMapper, SIGNAL(mapped(int)), m_tabs, SLOT(setCurrentIndex(int)) ); } - /* ======================== positionChanged ======================== +XXX: Contains a hack to fix a bug occuring on low-end graphics card that don't support +geometry shaders... Tabs index becomes invalid, and thus causes a segfault. +The fix is merely a correction of indices in case geometry shaders aren't present. +It is not meant to be an optimal fix, I didn't have time to delve into the code. +This should still work with geometry shaders present, though this is untested. */ void CMdiEditWindow::positionChanged( void ) { - QTextCursor cursor = m_editors[m_tabs-&gt;currentIndex()]-&gt;textCursor();
        + int index = m_tabs-&gt;currentIndex();
        + /**
        + * XXX: Hack to fix geometry shader bug
        + **/
        + if(!m_geometryShaderAvailable &amp;&amp; m_tabs-&gt;currentIndex() == 1) {
        + index = 2;
        + }
        + CSourceEdit *edit = m_editors[index];
        + QTextCursor cursor = edit-&gt;textCursor();
        int ln = cursor.blockNumber() + 1;
        int col = cursor.columnNumber() + 1;
        m_lineNumber-&gt;setText( "Ln: " + QString::number(ln) + " | Col: " + QString::number(col) );
        @@ -831,7 +844,7 @@ CSourceEdit* CMdiEditWindow::activeDocument( void )
        // do not type cast. does not hurt, since there are only 3 elements...
        for( int i = 0 ; i &lt; IShader::MAX_SHADER_TYPES ; i++ )
        {
        - if( m_editors[ i ] != NULL &amp;&amp;
        + if( m_editors[ i ] != NULL &amp;&amp;
        m_editors[ i ] == widget )
        {
        return m_editors[ i ];
        @@ -854,7 +867,7 @@ int CMdiEditWindow::tabToShader( int tabIndex )
        // look up the widget... it only take 3 loops...
        for( int i = 0 ; i &lt; IShader::MAX_SHADER_TYPES ; i++ )
        {
        - if( m_editors[ i ] != NULL &amp;&amp;
        + if( m_editors[ i ] != NULL &amp;&amp;
        m_editors[ i ] == widget )
        {
        return i;
        diff --git a/src/editwindow.h b/src/editwindow.h
        index 0a5fc20..33a8a9d 100644
        --- a/src/editwindow.h
        +++ b/src/editwindow.h
        @@ -305,6 +305,7 @@ private:
        // all documents
        CSourceEdit** m_editors; // [ IShader::MAX_SHADER_TYPES ]
        bool* m_attachToShader; // [ IShader::MAX_SHADER_TYPES ]
        + bool m_geometryShaderAvailable; // XXX: Hack to fix geometry shader bug on low end graphics card
         
        // actions
        QAction* m_actNextShader;


