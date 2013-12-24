Title: Using CMake
Date: 2009-12-27 
Tags: fotowall
Summary: CMake is a building toolkit for both Linux, Windows and Mac OS. It is somewhat similar to the autotools, but much more flexible. You'll learn the basis of how it works here!
disqus_identifier: geenux-using-cmake

Je me souviens encore des premier projets pour lesquels j’ai tenté de comprendre comment utiliser cmake pour créer les makefiles.  La doc est tout sauf claire, et le manque de tutoriels sur la base du fonctionnement de cmake manque cruellement. Je vais tâcher de remédier à ce souci, en expliquant comment compiler des projets simples avec cmake.

# Qu’est-ce que cmake ?

Il s’agit d’un outil permettant de ne pas avoir à écrire les Makefiles à la main. Il permet de rechercher automatiquement les librairies sur le systèmes, de régler les compilation en statique ou dynamique, de compiler aisément à partir d’un dossier séparé. C’est un réel plus pour la portabilité (cmake fonctionne sur de nombreux systèmes, et la plupart des modules peuvent trouver les lib aussi bien sous Windows, que GNU/Linux…).

Cmake permet de vous affranchir de la syntaxe immonde des makefiles, et de vous contenter de décrire la manière de compilation de votre programme, de conditionner la compilation…


# Un cmake minimal.

Tout d’abord, voici un exemple de CMakeFile.txt (c’est le fichier que cmake lit pour le convertir en makefile) permettant de compiler avec Boost.

    ::cmake
        cmake_minimum_required( VERSION 2.6 FATAL_ERROR )
 
        # search for Boost version 1.40
        # Components :
        #filesystem, iostreams, programoptions, python, regex, serialization, signals
        #system, thread, wave
        find_package( Boost 1.40.0 COMPONENTS regex signals FATAL_ERROR)
        link_directories ( ${Boost_LIBRARY_DIRS} )
        include_directories ( ${Boost_INCLUDE_DIRS} )
         
        SET (SOURCES
        main.cpp
        )
         
        SET (EXECUTABLE_NAME
        executable
        )
         
        add_executable (
        ${EXECUTABLE_NAME}
        ${SOURCES}
        )
         
        target_link_libraries (
        ${EXECUTABLE_NAME}
        ${Boost_LIBRARIES}
        )

Comme vous pouvez le constater dans cet exemple, cmake gère les variables, et sa syntaxe est assez simple. Étudions plus en détail ce fichier.

    ::cmake
        cmake_minimum_required( VERSION 2.6 FATAL_ERROR )

Cette ligne indique qu’il faut avoir la version 2.6 de cmake pour compiler, le FATAL_ERROR est facultatif, il indique à cmake de ne pas essayer de compiler et de stopper tout de suite.

    ::cmake
        find_package( Boost 1.40.0 COMPONENTS regex signals FATAL_ERROR)

Il s’agit d’une des fonctionnalités les plus intéressantes de cmake : la recherche des librairies. La fonctionnalité find_package va chercher un fichier (appelé module), permettant de rechercher la lib voulue nommée FindBoost.cmake. Chez moi ce fichier est dans "/usr/share/cmake-2.6/Modules/FindBoost.cmake".
(si vous ne le trouvez pas, un simple `locate FindBoost.cmake` devrait le trouver).
Pourquoi je vous indique ces détails sur le fichier ? Eh bien, parceque la lecture du fichier en question va vous fournir une mine d’information sur ce qu’il fait, quelles variables il définit, bref comment l’exploiter.
Voici quelques extraits du header de ce fichier :

    ::cmake
        # - Try to find Boost include dirs and libraries
        # Usage of this module as follows:
        #
        # == Using Header-Only libraries from within Boost: ==
        #
        #   find_package( Boost 1.36.0 )
        #   if(Boost_FOUND)
        #      include_directories(${Boost_INCLUDE_DIRS})
        #      add_executable(foo foo.cc)
        #   endif()
        #
        #
        # == Using actual libraries from within Boost: ==
        #
        #   set(Boost_USE_STATIC_LIBS   ON)
        #   set(Boost_USE_MULTITHREADED ON)
        #   find_package( Boost 1.36.0 COMPONENTS date_time filesystem system ... )
        #
        #   if(Boost_FOUND)
        #      include_directories(${Boost_INCLUDE_DIRS})
        #      add_executable(foo foo.cc)
        #      target_link_libraries(foo ${Boost_LIBRARIES})
        #   endif()
        #
        #
        # The components list needs to contain actual names of boost libraries only,
        # such as "date_time" for "libboost_date_time".  If you're using parts of
        # Boost that contain header files only (e.g. foreach) you do not need to
        # specify COMPONENTS.
        #
        # You should provide a minimum version number that should be used. If you provide this
        # version number and specify the REQUIRED attribute, this module will fail if it
        # can't find the specified or a later version. If you specify a version number this is
        # automatically put into the considered list of version numbers and thus doesn't need
        # to be specified in the Boost_ADDITIONAL_VERSIONS variable (see below).
        #
        # NOTE for Visual Studio Users:
        #     Automatic linking is used on MSVC &amp; Borland compilers by default when
        #     #including things in Boost.  It's important to note that setting
        #     Boost_USE_STATIC_LIBS to OFF is NOT enough to get you dynamic linking,
        #     should you need this feature.  Automatic linking typically uses static
        #     libraries with a few exceptions (Boost.Python is one).
        #
        #     Please see the section below near Boost_LIB_DIAGNOSTIC_DEFINITIONS for
        #     more details.  Adding a TARGET_LINK_LIBRARIES() as shown in the example
        #     above appears to cause VS to link dynamically if Boost_USE_STATIC_LIBS
        #     gets set to OFF.  It is suggested you avoid automatic linking since it
        #     will make your application less portable.
        [...]
        # Variables used by this module, they can change the default behaviour and
        # need to be set before calling find_package:
        #
        #   Boost_USE_MULTITHREADED      Can be set to OFF to use the non-multithreaded
        #                                boost libraries.  If not specified, defaults
        #                                to ON.
        #
        #   Boost_USE_STATIC_LIBS        Can be set to ON to force the use of the static
        #                                boost libraries. Defaults to OFF.
        #
        # Other Variables used by this module which you may want to set.
        #
        #   Boost_ADDITIONAL_VERSIONS    A list of version numbers to use for searching
        #                                the boost include directory.  Please see
        #                                the documentation above regarding this
        #                                annoying, but necessary variable <img src="http://s0.wp.com/wp-includes/images/smilies/icon_sad.gif?m=1129645325g" alt=":(" class="wp-smiley"> 
        #
        [...]
        #
        #   Boost_INCLUDE_DIRS                  Boost include directories: not cached
        #
        #   Boost_INCLUDE_DIR                   This is almost the same as above, but this one is
        #                                       cached and may be modified by advanced users
        #
        #   Boost_LIBRARIES                     Link to these to use the Boost libraries that you
        #                                       specified: not cached
        #
        #   Boost_LIBRARY_DIRS                  The path to where the Boost library files are.
        #
        #   Boost_VERSION                       The version number of the boost libraries that
        #                                       have been found, same as in version.hpp from Boost
        [...]
        #   Boost_${COMPONENT}_FOUND            True IF the Boost library "component" was found.
        #
        #   Boost_${COMPONENT}_LIBRARY          Contains the libraries for the specified Boost
        #                                       "component" (includes debug and optimized keywords
        #                                       when needed).

Grâce aux informations contenues ici, on pourra facilement construite un CMakeFile adapté à nos besoins.
Revenons à l’exemple :
find_package va utiliser le fichier indiqué plus haut pour rechercher boost, le module va définir de nombreuses variable (comme on voit dans le header ci-dessus), que l’on va utiliser pour la compilation.

    ::cmake 
        find_package( Boost 1.40.0 COMPONENTS regex signals FATAL_ERROR)
        link_directories ( ${Boost_LIBRARY_DIRS} )
        include_directories ( ${Boost_INCLUDE_DIRS} )k

La ligne link_directories indique que cmake devra lier l’exécutable avec la librairie boost, ${Boost_LIBRARY_DIRS} étant une variable définie par le module appelé par find_package.
La ligne include_directories fait de même pour le répertoire dans lequel les includes de boost sont.

    ::cmake 
        SET (SOURCES main.cpp autre.cpp)
        SET (EXECUTABLE_NAME executable)

On définit 2 variables SOURCES et EXECUTABLE_NAME, comme ça on aura juste à modifier à un seul endroit, et tout le reste sera modifié en conséquence.

    ::cmake
        add_executable (${EXECUTABLE_NAME} ${SOURCES})
        target_link_libraries (${EXECUTABLE_NAME} ${Boost_LIBRARIES})


add_executable indique à cmake qu’il faut compiler les sources contenues dans la variable SOURCE et créer un exécutable nommé par le nom défini dans la variable EXECUTABLE_NAME
target_link_libraries indique à cmake avec quelles librairies il doit lier.

Et voilà, vous avez un CMakeList pour compiler avec boost.

    ::bash
        mkdir build && cd build
        cmake ..
        make

Et voilà, les sources sont compilés dans le dossier build.


