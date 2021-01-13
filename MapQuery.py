from owslib.wms import WebMapService
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

''' 
# No Longer needed as database now uses GDA projection instead of MGA:

# from pyproj import Proj, transform
# from pyproj import datadir, datadir

def reproject(input_x, input_y):
    in_proj = Proj(init='epsg:7855')  # Input EPSG:   _MGA 2020 ZONE 55
    out_proj = Proj(init='epsg:4326')  # Output EPSG:  WGS 84

    output_y, output_x = transform(in_proj, out_proj, input_y, input_x)

    return output_x, output_y
'''


def get_map(coor_x, coor_y):

    # Ratio to keep: 0.4375 ; For changing x, y (Increase Y value then multiply by ratio to get X)
    zoom_ratio = 0.4375  # Default: 0.4375,  !!!! Make this a config setting
    zoom_y = 0.003000  # 0.003000 = less lot/house number overlap, !!!! make this a config setting
    zoom_x = zoom_y * zoom_ratio

    x_upper, y_upper = (coor_x - zoom_x), (coor_y + zoom_y)
    x_lower, y_lower = (coor_x + zoom_x), (coor_y - zoom_y)

    wms = WebMapService(
        'http://services.land.vic.gov.au/catalogue/publicproxy/guest/dv_geoserver/wms?request=getCapabilities',
        version='1.3.0')

    # Below is used for development purposes only:
    # for i in wms.contents:
    #    print(i)

    # Possible layer: VMADD_ADDRESS: VMADD_ADDRESS_NO

    # featureinfo = wms.getfeatureinfo(layers=['VMPROP_PROPERTY_ADDRESS'],
    #                                 xy=[x, y])

    # print(wms.getOperationByName('GetMap').formatOptions)

    img = wms.getmap(layers=['VMPROP_PROPERTY_ADDRESS',         # First one in list is highest priority and overlaps.
                             'VMPROP_ANNOTATION_TEXT',
                             'VMTRANS_TR_ROAD_LOCAL',
                             'VMTRANS_TR_ROAD',
                             'VMTRANS_TR_ROAD_PROPOSED'],
                     format='image/png',
                     bbox=(y_lower, x_upper, y_upper, x_lower, 'CRS:84'),
                     srs='EPSG:4326',
                     size=((3508-20)//2, (2480-501)//2),          # !!!! Make this a config setting?
                     transparent=False,
                     styles=['VMPROP_PROP_ADDRESS_CSS',
                             'VMPROP_ANNOTATION_TEXT',
                             'VMTRANS_TR_ROAD',
                             'VMTRANS_TR_ROAD',
                             'line']
                     )
    out = open('MapData/Temp_Map.png', 'wb')             # !!!! This will need to be custom named to the site
    out.write(img.read())
    out.close()


def edit_map(site_name, map_ref, x_c, y_c):

    # Notes:
    # A4 = 3508, 2480
    # (3508-20), (2480-501) end size of map from wms

    joined_coordinates = str(x_c) + ', ' + str(y_c)

    base_image_offset = 491

    # Open all images to be used
    base_image = Image.new('RGBA', (3508, 2480), (0, 0, 0, 0))
    map_image = Image.open('MapData/Temp_Map.png')
    eagle_logo = Image.open('MapData/Eagle_Logo.png')
    point_image = Image.open('MapData/Map_Point.png')
    base_map_layout = Image.open('MapData/Base_Map.png')

    # Resize map from wms
    width, height = map_image.size
    map_image = map_image.resize((width * 2, height * 2))

    # Resize point image to add to map:
    point_image = point_image.resize((point_image.width * 4, point_image.height * 4))

    # Adding image layers to main image:
    base_image.paste(base_map_layout, (0, 0))
    base_image.paste(map_image, (10, base_image_offset))
    base_image.paste(eagle_logo, (90, 70), mask=eagle_logo)
    base_image.paste(point_image, (((base_image.width - point_image.width) // 2),
                                   (((base_image.height + base_image_offset) - point_image.height) // 2)),
                     mask=point_image)

    # Add Legend to map

    # Add Site Text
    draw = ImageDraw.Draw(base_image)
    font = ImageFont.truetype('MapData/NIOBRG__.ttf', 70)
    draw.text((90, 340), site_name, (0, 0, 0), font=font)       # Draws location + string + color + font

    # Add Coordinates + Melways Text
    font = ImageFont.truetype('MapData/NIOBRG__.ttf', 100)
    draw.text((2450, 90), map_ref, (0, 0, 0), font=font)
    draw.text((2450, 210), joined_coordinates, (0, 0, 0), font=font)

    # Save and export combined image
    base_image.save("MapData/Combine_Map.png")

