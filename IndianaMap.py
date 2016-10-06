# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IndianaMap
                                 A QGIS plugin
 Integrate web services for approximately 300 data layers
                              -------------------
        begin                : 2016-06-23
        git sha              : $Format:%H$
        copyright            : (C) 2016 by IU UITS GIS
        email                : jppeters@iu.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import ctypes
import webbrowser
from PyQt4.QtCore import * #QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import * #QAction, QIcon
from qgis.core import * #QgsMapLayerRegistry
from qgis import *#utils#, resources
#from qgis import resources
from qgis.utils import *#iface
#from qgis.core import QgsRasterLayer
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from IndianaMap_dialog import IndianaMapDialog
import os.path


class IndianaMap:
    """QGIS Plugin Implementation."""

    
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'IndianaMap_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = IndianaMapDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&IndianaMap Data Plugin')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'IndianaMap')
        self.toolbar.setObjectName(u'IndianaMap')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('IndianaMap', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/IndianaMap/addContent.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&IndianaMap Data Plugin'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def doISDP(self, event):
            my_crs = core.QgsCoordinateReferenceSystem(26916,core.QgsCoordinateReferenceSystem.EpsgCrsId)
            iface.mapCanvas().mapRenderer().setDestinationCrs(my_crs)
            extent = iface.mapCanvas().extent().toString()
            newext = extent.replace(":", ",")
            my_list = newext.split(",")
            print my_list[0]
            print my_list[1]
            print my_list[2]
            print my_list[3]
            my_list = [x.strip(' ') for x in my_list]
            webbrowser.open_new("https://gisdb.uits.indiana.edu/ISDP/filelist.php?xmin="+my_list[0]+"&ymin="+my_list[1]+"&xmax="+my_list[2]+"&ymax="+my_list[3]+"")
            #webbrowser.open_new("http://maps.indiana.edu")
    def doDownload(self, event):
            extent = iface.mapCanvas().extent().toString()
            print extent
            comboBoxText = self.dlg.comboBox.currentText()
            webbrowser.open_new("http://maps.indiana.edu/download/"+comboBoxText+".zip")
    def doLayerGallery(self, event):
            extent = iface.mapCanvas().extent().toString()
            print extent
            comboBoxText = self.dlg.comboBox.currentText()
            webbrowser.open_new("https://maps.indiana.edu/LayerGallery.html")
    def doInMap(self, event):
            extent = iface.mapCanvas().extent().toString()
            print extent
            comboBoxText = self.dlg.comboBox.currentText()
            webbrowser.open_new("https://maps.indiana.edu/LayerGallery.html")
    def run(self):
        #if iface.mapCanvas().mapRenderer().hasCrsTransformEnabled():
        
        """Run method that performs all the real work"""
        # show the dialog
        
        self.dlg.label_2.mousePressEvent = self.doInMap
        self.dlg.label_3.mousePressEvent = self.doDownload
        self.dlg.label.mousePressEvent = self.doLayerGallery
        self.dlg.label_4.mousePressEvent = self.doISDP
        self.dlg.label_7.mousePressEvent = self.doISDP
        
        
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        comboBoxText = self.dlg.comboBox.currentText()
        comboBoxText2 = comboBoxText.replace("/", "_", 1)
        #checkBox = self.dlg.checkBox
        # See if OK was pressed
        if comboBoxText == 'Basemaps/Streets':
            service = 'contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/jpeg&layers=0&styles=&url=http://maps.indiana.edu/arcgis/services/Basemaps/Streets/MapServer/WMSServer'
            #service = 'contextualWMSLegend=0&crs=EPSG:26916&dpiMode=7&featureCount=10&format=image/png&layers='+comboBoxText2+'&styles=default&tileMatrixSet=default028mm&url=http://maps.indiana.edu/arcgis/rest/services/'+comboBoxText+'/MapServer/WMTS/1.0.0/WMTSCapabilities.xml'
            rlayer = QgsRasterLayer(service, comboBoxText, "wms")
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)
        elif comboBoxText == 'Basemaps/Topos':
            service = 'contextualWMSLegend=0&crs=EPSG:26916&dpiMode=7&featureCount=10&format=image/png&layers=Basemaps_Topos&styles=default&tileMatrixSet=default028mm&url=http://maps.indiana.edu/arcgis/rest/services/Basemaps/Topos/MapServer/WMTS/1.0.0/WMTSCapabilities.xml'
            #service = 'contextualWMSLegend=0&crs=EPSG:26916&dpiMode=7&featureCount=10&format=image/png&layers='+comboBoxText2+'&styles=default&tileMatrixSet=default028mm&url=http://maps.indiana.edu/arcgis/rest/services/'+comboBoxText+'/MapServer/WMTS/1.0.0/WMTSCapabilities.xml'
            rlayer = QgsRasterLayer(service, comboBoxText, "wms")
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)#contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/jpeg&layers=0&styles=&url=http://maps.indiana.edu/arcgis/services/Basemaps/PLSS/MapServer/WMSServer?
        elif comboBoxText == 'Basemaps/PLSS':
            service = 'contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/jpeg&layers=0&styles=&url=http://maps.indiana.edu/arcgis/services/Basemaps/PLSS/MapServer/WMSServer'
            #service = 'contextualWMSLegend=0&crs=EPSG:26916&dpiMode=7&featureCount=10&format=image/png&layers='+comboBoxText2+'&styles=default&tileMatrixSet=default028mm&url=http://maps.indiana.edu/arcgis/rest/services/'+comboBoxText+'/MapServer/WMTS/1.0.0/WMTSCapabilities.xml'
            rlayer = QgsRasterLayer(service, comboBoxText, "wms")
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)      
        else:
            if result:
                service = 'crs=EPSG:26916&dpiMode=7&featureCount=10&format=image/png&layers=0&styles=&url=https://maps.indiana.edu/arcgis/services/'+comboBoxText+'/MapServer/WMSServer'
                #service = 'crs=EPSG:26916&dpiMode=7&featureCount=10&format=image/png&layers=0&layers=1&layers=2&layers=3&layers=4&layers=5&layers=6&layers=7&layers=8&layers=9&layers=10&layers=11&layers=12&layers=13&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&url=https://maps.indiana.edu/arcgis/services/'+comboBoxText+'/MapServer/WMSServer'
                #service = 'contextualWMSLegend=0&crs=EPSG:26916&dpiMode=7&featureCount=10&format=image/png&layers='+comboBoxText2+'&styles=default&tileMatrixSet=default028mm&url=http://maps.indiana.edu/arcgis/rest/services/'+comboBoxText+'/MapServer/WMTS/1.0.0/WMTSCapabilities.xml'
                rlayer = QgsRasterLayer(service, comboBoxText, "wms")
                QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            #rlayer2 = QgsRasterLayer('plugins/IndianaMap/arc.xml', "wmts master example", "wms")
            #QgsMapLayerRegistry.instance().addMapLayer(rlayer2)
            # Do something useful here - delete the line containing pass and
            #gdal_translate "https://maps.indiana.edu/arcgis/rest/services/Reference/LiDAR_Color_Hillshade/MapServer?f=json&pretty=true" s.xml -of WMS# substitute with your code.
            #iface.addRasterLayer("https://maps.indiana.edu/arcgis/services/"+comboBoxText+"/MapServer/WMSServer?f=json&pretty=true&spatialReference=wkid'26916'",comboBoxText)
            #service2 = 'crs=EPSG:26916&dpiMode=7&featureCount=10&format=image/png&layers=0&styles=&url=https://maps.indiana.edu/arcgis/services/Demographics/Census_Counties/MapServer/WMSServer?crs=EPSG:26916&dpiMode=7&featureCount=10&format=image/png&layers=99&styles='
            #rlayer2 = QgsRasterLayer(service2, "Census Counties", "wms")
            #QgsMapLayerRegistry.instance().addMapLayer(rlayer2)
            #iface.addRasterLayer("https://maps.indiana.edu/arcgis/rest/services/Reference/LiDAR_Color_Hillshade/MapServer?f=json&pretty=true","raster") #urlWithParams = 'url=http://maps.indiana.edu/arcgis/services/Reference/LiDAR_Color_Hillshade/MapServer/WMSServer?request=GetCapabilities&service=WMS'
            #iface.addRasterLayer('rlayer')
            #urlWithParams = 'url=http://wms.jpl.nasa.gov/wms.cgi&layers=global_mosaic&styles=pseudo&format=image/jpeg&crs=EPSG:4326'
            #rlayer = QgsRasterLayer(urlWithParams, 'some layer name', 'wms')
                if not rlayer.isValid():
                    print "Layer failed to load!"#iface.addRasterLayer("/N/u/jppeters/Karst/test2.tif", "layer name you like")
