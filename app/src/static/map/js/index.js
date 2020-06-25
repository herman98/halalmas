$(document).ready(function() {

  var DATA = {
    // this is for production and tequila
    url_web: 'https://xwork.co',
    url: 'https://app.xwork.co',
    // url_web: 'https://wine.xwork.co',
    // url: 'http://tequila.xwork.co',
    client_id: '1',
    client_secret: 'quZ8CX2thlcgzKlKz0D3_okfPwNUCaZ7WEejCPS3LHPhp4h2sAvBC4zL',
    grant_type: 'client_credentials',

    // this is for development
    // url: 'http://vodka.xwork.co',
    // client_id: 'N0d3.1bddF8c08f53Ed1612E94.dd8d_D48',
    // client_secret: '_8cD4e5bad3db751F616edDD3Ae_24FA694F4173441e96377eE73f32DFBc',
    // grant_type: 'client_credentials',

    center: {
      lat: -6.2299792,
      lng: 106.8266873
    }
  };

  var map;
  var buildingMarkers;

  function showPage() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("mapContainer").style.display = "block";
  }

  function callbackInitMap(res) {
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 5,
      center: DATA.center,
      scrollwheel: false
    });

    var buildings = res.buildings;
    var rooms = res.rooms;

    var data = [];

    for(var x=0; x<buildings.length; x++) {
      var building = buildings[x];
      building.lng = buildings[x].lon;
      building.rooms = [];
      for(var y=0; y<rooms.length; y++) {
        if(building.id == rooms[y].id_building) {
          building.rooms.push(rooms[y]);
        }
      }
      data.push(building);
    }

    var infoWindow = new google.maps.InfoWindow({maxWidth: 250});

    buildingMarkers = data.map(function(item, i) {
      var marker = new MarkerWithLabel({
        position: item,
        icon: 'static/map/img/icon/icon_location_tower.png?i=' + item.id,
        labelContent: item.rooms.length + ' room',
        labelAnchor: new google.maps.Point(30, 22),
        labelClass: 'marker-label', // the CSS class for the label
        labelStyle: {opacity: 1.0},
        optimized: false,
        zIndex: 1
      });

      var roomImageFirst = [];
      item.rooms.map(function(room, i) {
        var urlImg = room.cimages.url+'/'+room.cimages.room_id+'/'+room.cimages.images[0]+'/'+room.cimages.room_id+'_'+room.cimages.images[0]+'.'+room.cimages.size[(room.cimages.size.length-1)]+'.'+room.cimages.image_format;
        var el = '<img class="infowindow-image-thumb-container" src="'+urlImg+'" />';
        roomImageFirst.push(el);
      })
      roomImageFirst.join(" ");

      MarkerLabel_.prototype.onRemove = function () {
        var i;
        if (this.labelDiv_.parentNode) {
          this.labelDiv_.parentNode.removeChild(this.labelDiv_);
        } // Remove event listeners:
        if (this.listeners_) {
          for (i = 0; i < this.listeners_.length; i++) {
            google.maps.event.removeListener(this.listeners_[i]);
          }
        }
      };

      // handle the marker click
      google.maps.event.addListener(marker, 'click', function () {
        infoWindow.setContent('<a>' +
                                '<div class="infowindow" style="width: 100%">' +
                                  '<div style="width: 40%;vertical-align: top; display: inline-block; margin-right: 10px">' +
                                    '<img class="infowindow-image-container infowindow-' + item.id + '" src="' + item.picture + '" />' +
                                  '</div>' +
                                  '<div style="width: calc(60% - 10px);display: inline-block;"; display: inline-block; vertical-align: top">' +
                                    '<h2 style="color: #333;">' + item.name + '</h2>' +
                                    '<div class="infowindow-image-thumb-container-wrapper">' +
                                      roomImageFirst +
                                    '</div>' +
                                  '</div>' +
                                  '<div class="infowindow-address">' + item.address + '</div>' +
                                '</div>' +
                              '</a>')

        infoWindow.open(map, this);

        $('img').on('error', function () {
          $(this).attr('src', 'static/map/img/building-error.png');
        })
        if (!(item.goto_room_list == '')) {
          $('.infowindow-' + item.id).click(callbackClickBuilding(item));
        }
        setRoomListFromBuilding(item);
      })

      return marker
    });

    var markerCluster = new MarkerClusterer(map, buildingMarkers, {
      imagePath: 'static/map/lib/img/cluster/m'
    });

    initializeSearchBox();
    showPage();
  }

  function callbackClickBuilding (data) {
    return function () {
      var prettyBuilding = (data.name.split(" ").join("-")).toLowerCase();
      var urlBuilding = DATA.url_web + '/id/room-listing/building/'+prettyBuilding+'-'+data.id;
      window.open(urlBuilding, '_blank')
    }
  }

  function setRoomListFromBuilding (data) {
    return function () {
      // var url = data.goto_room_list
      // window.open(url, '_blank')
      alert("setRoomListFromBuilding", JSON.stringify(data));
    }
  }

  function initializeAllData(callback) {
    $.ajax({
      type: 'POST',
      url: DATA.url + '/api/v1/client/oauth',
      data: {
        'grant_type': DATA.grant_type,
        'client_id': DATA.client_id,
        'client_secret': DATA.client_secret
      },
      success: function(res) {
        $.ajax({
          headers: {
            'Authorization': 'bearer ' + res.access_token
          },
          type: 'GET',
          url: DATA.url + '/api/v2/rooms/search?lat=-6.2069127&lon=106.8334877&results_per_page=10000&radius=10000',
          success: callback
        });
      }
    });
  }

  function initializeSearchBox() {
    var input = document.getElementById('searchTextField');
    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setComponentRestrictions({'country': ['id']});

    autocomplete.addListener('place_changed', function() {
      var place = autocomplete.getPlace();
      if (!place.geometry) {
        // User entered the name of a Place that was not suggested and
        // pressed the Enter key, or the Place Details request failed.
        window.alert("No details available for input: '" + place.name + "'");
        return;
      }
      // If the place has a geometry, then present it on a map.
      if (place.geometry.viewport) {
        map.fitBounds(place.geometry.viewport);
        map.setZoom(15);
      } else {
        map.panTo(place.geometry.location);
        map.setZoom(15);
      }

      var address = '';
      if (place.address_components) {
        address = [
          (place.address_components[0] && place.address_components[0].short_name || ''),
          (place.address_components[1] && place.address_components[1].short_name || ''),
          (place.address_components[2] && place.address_components[2].short_name || '')
        ].join(' ');
      }
    });
  }

  initializeAllData(callbackInitMap);
})
