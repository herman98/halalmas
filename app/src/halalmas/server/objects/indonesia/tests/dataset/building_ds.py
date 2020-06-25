from django.contrib.gis.geos import Point


kelurahan_buildings = {
    "kemanggisan": [
        {
            "name": "Slipi jaya",
            "address": "Jl. Anggrek Neli Murni No.89, RT.12/RW.1, Kemanggisan, Palmerah, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11480",
            "coord_google": Point(106.7929603, -6.1893417)
        }
    ],
    "kota bambu utara": [
        {
            "name": "Rumah Sakit Anak dan Bunda Harapan Kita",
            "address": "Jl. Letjen S. Parman No.Kav 87, RT.1/RW.8, Kota Bambu Utara, Palmerah, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11420",
            "coord_google": Point(106.7957538, -6.1850721)
        },
    ],
    "kota bambu selatan": [
        {
            "name": "Rumah Sakit Kanker Dharmais",
            "address": "Slipi, Jalan Letjen Jend. S. Parman No.84-86, RT.4/RW.9, Kota Bambu Sel., Palmerah, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta",
            "coord_google": Point(106.7959019, -6.1869858)
        },
    ],
    "palmerah": [
        {
            "name": "SMP Regina Pacis",
            "address": "Jalan Palmerah Utara I No.1, RT.1/RW.5, Palmerah, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11480",
            "coord_google": Point(106.7948269, -6.2014052)
        },
        {
            "name": "Kolary Coffee & Kitchen",
            "address": "Jl. Raya Kb. Jeruk No.8A, RT.6/RW.12, Sukabumi Utara, Kb. Jeruk, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11480",
            "coord_google": Point(106.7815178, -6.2019456)
        },
        {
            "name": "Binus Syahdan",
            "address": "Jalan Kyai Haji Syahdan No.9, RT.6/RW.12, Kemanggisan, Palmerah, RT.6/RW.12, Palmerah, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11480",
            "coord_google": Point(106.7832843, -6.2002502)
        },
    ],
    "slipi": [
        {
            "name": "Wisma 76",
            "address": "Jl. Letjen S. Parman No.Kav. 76, RT.4/RW.3, Slipi, Palmerah, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11410",
            "coord_google": Point(106.796126, -6.1908949)
        },
        {
            "name": "Wisma 77",
            "address": "Jl. Letjen S. Parman No.Kav. 76, RT.4/RW.3, Slipi, Palmerah, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11410",
            "coord_google": Point(106.797167, -6.19045)
        },
        {
            "name": "CITICON",
            "address": "Jl. Letjen S. Parman No.Kav 72, RT.4/RW.3, Slipi, Palmerah, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11410",
            "coord_google": Point(106.7955234, -6.1927019)
        },
    ],
    "kebon jeruk": [
        {
            "name": "BINUS Anggrek Campus",
            "address": "Jalan Anggrek Cakra No.1A, RT.4/RW.6, Kebon Jeruk, RT.1/RW.9, Kb. Jeruk, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11540",
            "coord_google": Point(106.779403, -6.2018048)
        },
        {
            "name": "Sekolah Sang Timur",
            "address": "Jalan Karmel Raya No.8, RT.2/RW.4, Kebon Jeruk, RT.2/RW.4, Kb. Jeruk, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11530",
            "coord_google": Point(106.7776448, -6.1900073)
        },
    ],
}

BUILDING_JAKBAR = []
for _, building in kelurahan_buildings.items():
    BUILDING_JAKBAR += building

KELURAHAN = list(kelurahan_buildings.keys())
