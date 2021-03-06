#  Gispo Ltd., hereby disclaims all copyright interest in the program GemeindescanExporter
#  Copyright (C) 2020 Gispo Ltd (https://www.gispo.fi/).
#
#
#  This file is part of GemeindescanExporter.
#
#  GemeindescanExporter is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  GemeindescanExporter is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with GemeindescanExporter.  If not, see <https://www.gnu.org/licenses/>.
import tempfile

import pytest
from qgis.core import QgsProject, QgsVectorLayer, QgsVectorDataProvider

from ..qgis_plugin_tools.testing.utilities import get_qgis_app
from ..qgis_plugin_tools.tools.resources import plugin_test_data_path

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()

QGIS_INSTANCE = QgsProject.instance()


@pytest.fixture
def new_project() -> None:
    """Initializes new iface project"""
    yield IFACE.newProject()


@pytest.fixture(scope='session')
def test_gpkg():
    return plugin_test_data_path('test_data_4326.gpkg')


@pytest.fixture
def layer_simple_poly(test_gpkg):
    name = 'simple_poly'
    layer = get_layer(name, test_gpkg)
    return layer


@pytest.fixture
def layer_points(test_gpkg):
    name = 'school_point'
    layer = get_layer(name, test_gpkg)
    return layer


@pytest.fixture
def layer_lines(test_gpkg):
    name = 'roads_line'
    layer = get_layer(name, test_gpkg)
    return layer


@pytest.fixture
def categorized_poly(layer_simple_poly):
    add_layer(layer_simple_poly)
    style_file = plugin_test_data_path('style', 'categorized_poly.qml')
    msg, succeeded = layer_simple_poly.loadNamedStyle(style_file)
    assert succeeded, msg
    return layer_simple_poly


@pytest.fixture
def centroid_poly(layer_simple_poly):
    add_layer(layer_simple_poly)
    style_file = plugin_test_data_path('style', 'centroid_poly.qml')
    msg, succeeded = layer_simple_poly.loadNamedStyle(style_file)
    assert succeeded, msg
    return layer_simple_poly


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory(dir=plugin_test_data_path()) as tmpdirname:
        yield tmpdirname


@pytest.fixture
def layer_empty_poly(tmp_dir, layer_simple_poly):
    dp: QgsVectorDataProvider = layer_simple_poly.dataProvider()
    layer = QgsVectorLayer('Polygon', 'test_poly', 'memory')
    layer.setCrs(dp.crs())
    assert layer.isValid()
    return layer


@pytest.fixture
def layer_empty_points(tmp_dir, layer_points):
    dp: QgsVectorDataProvider = layer_points.dataProvider()
    layer = QgsVectorLayer('Point', 'test_point', 'memory')
    layer.setCrs(dp.crs())
    assert layer.isValid()
    return layer


@pytest.fixture
def layer_empty_lines(tmp_dir, layer_lines):
    dp: QgsVectorDataProvider = layer_lines.dataProvider()
    layer = QgsVectorLayer('LineString', 'test_lines', 'memory')
    layer.setCrs(dp.crs())
    assert layer.isValid()
    return layer


# Helper functions


def get_layer(name: str, gpkg):
    layer = QgsVectorLayer(f'{gpkg}|layername={name}', name, 'ogr')
    assert layer.isValid()
    return layer


def add_layer(layer: QgsVectorLayer) -> None:
    initial_layers = QGIS_INSTANCE.mapLayers()
    QGIS_INSTANCE.addMapLayer(layer, False)
    assert len(QGIS_INSTANCE.mapLayers()) > len(initial_layers)
