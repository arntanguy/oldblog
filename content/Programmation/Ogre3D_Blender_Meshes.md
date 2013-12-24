Title: Créez Vos Mesh Ogre Sous Blender !
Date: 2010-03-04 
Tags: blender, ogre3D, 3D
Summary: Explains how to create UV-mapped models using blender, and export them for Ogre3D engine.
disqus_identifier: geenux-create-mesh-ogre-blender

Si vous aimez le logiciel de modélisation 3D Blender, vous serez sans doute ravi de l’utiliser pour créer votre monde dans votre jeu utilisant le moteur Ogre.
La bonne nouvelle, c’est que c’est d’une simplicité impressionnante, je vais profiter de ce billet pour me faire un petit mémo sur comment faire, ainsi que comment utiliser la technique de l’UV mapping avec Blender (je débute avec la 3D, que ça soit en programmation ou modélisation).

L’exemple présenté ici sera fait sur un simple cube, que l’on va texturer, et intégrer dans un projet Ogre.

# Installation du script d’exportation OGRE Meshes Exporter
## Sous Ubuntu

Tout d’abord, vous aurez besoin du script d’exportation pour Ogre. Sous Ubuntu pour l’installer, il suffit de faire

    ::bash
        sudo aptitude install blender-ogrexml

## Sous une autre distribution

Si vous avez une autre distribution, voici comment installer le script.

Téléchargez [OGRE Meshes Exporter](http://www.xullum.net/lefthand/downloads/temp/BlenderExport.zip)
Copiez ogremeshesexporter.py et les sous-dossiers dans `~/.blender/scripts`

Note : Vous devez aussi avoir python 2.6.4 installé pour que le script fonctionne.


# Création du cube et UV mapping

* Ouvrez Blender, créez un cube dans une nouvelle scène.
* Déplacez votre curseur sur la limite supérieure de la zone de modélisation jusqu’à voire une double flèche. Clic droit, puis clic gauche sur Split Area, puis clic gauche pour valider.
* Maintenant, dans la nouvelle fenêtre créé, passez en mode UV/ImageEditor

[![Sélection de l'UV
Mapping]({filename}/images/programmation/ogre3d/blender/uv_editor2.png)]({filename}/images/programmation/ogre3d/blender/uv_editor2.png)


* Retournez dans la vue 3D, passez en mode editing (touche tab), sélectionnez tout le cube

* Ensuite, faites U -> Unwrap (smart projection).
Smart projection est souvent la méthode de déroulement donnant les meilleurs résultats.

* Faites ensuite Image -> Open (Alt+O) et ouvrez une image de votre choix qui vous servira de texture. Vous pouvez en trouver dans le répertoire OGRE/media/materials/textures…
Une image apparait alors dans la partie de l’UV mapping. Normallement, les vues planes des faces du cubes devraient coincider avec la taille de l’image, si ce n’est pas le cas, sélectionnez toutes les faces dans la partie UV (touche A) puis redimensionnez les en utilisant la touche s.

On obtient


[![Dépliage du Cube]({filename}/images/programmation/ogre3d/blender/uv_editor2.png)]({filename}/images/programmation/ogre3d/blender/uv_editor2.png)
[![Résultat]({filename}/images/programmation/ogre3d/blender/uv_editor3.png)]({filename}/images/programmation/ogre3d/blender/uv_editor3.png)


* Allez dans la vue 3D, et faites Alt+Z pour passer en mode texturé. Normalement vous devriez voir la texture.
* Il ne reste plus qu’à assigner un matériau au cube, et à exporter.
Ouvrez le panneau Shading (F5), puis créez un nouveau matériau.
Cliquez sur Tex Face.


## Exportation

Faites Fichier->Exporter->Ogre Meshes.
Là, vous avez la fenêtre du bas qui se modifie. Cliquez sur « Game Engine Materials » et « OgreXMLConverter ». Le fait de sélectionner OgreXMLConverter appellera automatiquement le programme d’Ogre du même nom qui est chargé de convertir le fichier XML du mesh en des fichiers de mesh que le moteur comprend.
Cliquez sur « Exporter ».


[![Export]({filename}/images/programmation/ogre3d/blender/export.png)]({filename}/images/programmation/ogre3d/blender/export.png)

Sublime, magnifique, perfect, vous venez de créer votre premier Mesh pour OGRE. Mais comment l’utiliser maintenant ? Suivez le guide.


# Utiliser le mesh dans OGRE

Dans cette partie, je supposerai que vous connaissez au moins les bases de OGRE, c’est à dire les premiers tutoriels du wiki officiel, au moins jusqu’à la partie permettant de charger un mesh.

Tout d’abord, il va falloir placer les fichiers où il faut, c’est à dire… où vous voulez. Je vous conseille néamoins de respecter la structure habituelle de OGRE, c’est à dire

~~~~
    - Ogre (un dossier dans lequel vous placerez vos mesh, par exemple dans le répertoire de votre jeu, où ailleurs).
    —> models : vous placerez dans ce répertoire le fichier Cube.001.mesh qui a été généré par le script d’exportation
    —-> materials : ce répertoire contient les textures, scripts, enfin bref infos sur l’apparence
    ———-> textures : placez ici votre texture
    ———-> scripts : placez ici le fichier Scene.material généré par l’exportation
~~~~

Maintenant, il va falloir dire à Ogre où trouver les fichiers. Pour celà, modifiez le fichier ressource.cfg comme suitDans cette partie, je supposerai que vous connaissez au moins les bases de OGRE, c’est à dire les premiers tutoriels du wiki officiel, au moins jusqu’à la partie permettant de charger un mesh.

Tout d’abord, il va falloir placer les fichiers où il faut, c’est à dire… où vous voulez. Je vous conseille néamoins de respecter la structure habituelle de OGRE, c’est à dire

~~~~
    - Ogre (un dossier dans lequel vous placerez vos mesh, par exemple dans le répertoire de votre jeu, où ailleurs).
    —> models : vous placerez dans ce répertoire le fichier Cube.001.mesh qui a été généré par le script d’exportation
    —-> materials : ce répertoire contient les textures, scripts, enfin bref infos sur l’apparence
    ———-> textures : placez ici votre texture
    ———-> scripts : placez ici le fichier Scene.material généré par l’exportation
~~~~

Maintenant, il va falloir dire à Ogre où trouver les fichiers. Pour celà, modifiez le fichier ressource.cfg comme suit

    ::cfg
        # Resources required by the sample browser and most samples.
        [Essential]
        Zip=/usr/share/OGRE/media/packs/SdkTrays.zip
        FileSystem=/usr/share/OGRE/media/thumbnails
         
        # Common sample resources needed by many of the samples.
        # Rarely used resources should be separately loaded by the
        # samples which require them.
        [Popular]
        FileSystem=/usr/share/OGRE/media/fonts
        FileSystem=/usr/share/OGRE/media/materials/programs
        FileSystem=/usr/share/OGRE/media/materials/scripts
        FileSystem=/usr/share/OGRE/media/materials/textures
        FileSystem=/usr/share/OGRE/media/materials/textures/nvidia
        FileSystem=/usr/share/OGRE/media/models
        FileSystem=/usr/share/OGRE/media/particle
        FileSystem=/usr/share/OGRE/media/DeferredShadingMedia
        FileSystem=/usr/share/OGRE/media/PCZAppMedia
        FileSystem=/usr/share/OGRE/media/RTShaderLib
         
        # MODIFIEZ ICI : mettez le chemin des répertoires que vous venez de créer
        FileSystem=/media/data/programmation/3D/ogre/media/materials/scripts
        FileSystem=/media/data/programmation/3D/ogre/media/materials/textures
        FileSystem=/media/data/programmation/3D/ogre/media/models
         
        Zip=/usr/share/OGRE/media/packs/cubemap.zip
        Zip=/usr/share/OGRE/media/packs/cubemapsJS.zip
        Zip=/usr/share/OGRE/media/packs/dragon.zip
        Zip=/usr/share/OGRE/media/packs/fresneldemo.zip
        Zip=/usr/share/OGRE/media/packs/ogretestmap.zip
        Zip=/usr/share/OGRE/media/packs/ogredance.zip
        Zip=/usr/share/OGRE/media/packs/Sinbad.zip
        Zip=/usr/share/OGRE/media/packs/skybox.zip
         
        [General]
        FileSystem=/usr/share/OGRE/media

Plus qu’à tester ça sur un exemple, prenons celui du wiki officiel :

    ::cpp
        #include "ExampleApplication.h"
        class TutorialApplication : public ExampleApplication
        {
        protected:
        public:
            TutorialApplication()
            {
            }
         
            ~TutorialApplication()
            {
            }
        protected:
            void createScene(void)
            {
                mSceneMgr->setAmbientLight( ColourValue( 1, 1, 1 ) );
                Entity *ent1 = mSceneMgr->createEntity( "Test", "Cube.001.mesh" );
                SceneNode *node1 = mSceneMgr->getRootSceneNode()->createChildSceneNode( "TestNode" );
                node1->attachObject( ent1 );
            }
        };
         
        #if OGRE_PLATFORM == OGRE_PLATFORM_WIN32
        #define WIN32_LEAN_AND_MEAN
        #include "windows.h"
         
        INT WINAPI WinMain( HINSTANCE hInst, HINSTANCE, LPSTR strCmdLine, INT )
        #else
        int main(int argc, char **argv)
        #endif
        {
            // Create application object
            TutorialApplication app;
         
            try {
                app.go();
            } catch( Exception& e ) {
        #if OGRE_PLATFORM == OGRE_PLATFORM_WIN32
                MessageBox( NULL, e.what(), "An exception has occurred!", MB_OK | MB_ICONERROR | MB_TASKMODAL);
        #else
                fprintf(stderr, "An exception has occurred: %s\n",
                        e.what());
        #endif
            }
         
            return 0;
        }

Voilà, plus qu’à compiler, et à lancer le programme. Normallement, sous vos yeux ébahis, le cube apparait, texturé tout comme il faut.

# Problèmes

Voici quelques problèmes que j’ai rencontré, et comment les éviter :

* Si l’application ne démarre pas, vous avez probablement oublié de placer le fichier mesh Cube.001.mesh dans votre répertoire models/, ou alors vous n’avez pas spécifié correctement sa position dans le fichier ressources.cfg
* Si le cube n’est pas texturé, vérifiez que vous avez bien un fichier Scene.material dans votre dossier script, et que son emplacement est correctement spécifié dans le fichier ressources.cfg

Amusez vous bien, et si je n’ai pas été clair, n’hésitez pas à demander des précisions dans les commentaires.
