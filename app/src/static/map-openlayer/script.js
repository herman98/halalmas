createAxios()
initMap()

function createAxios() {
  if (!axios) {
    return setTimeout(function() {
      return createAxios()
    }, 200)
  } else {
    if (window.localStorage.token && JSON.parse(window.localStorage.token).exp > new Date().getTime()) {
      window._axios = axios.create({
        baseURL: 'https://app.xwork.co/api',
        timeout: 180000,
        headers: {
          Authorization: 'Bearer ' + JSON.parse(window.localStorage.token).clientToken
        }
      })

      getBuilding()
      initSearch()
    } else {
      window._axios = axios.create({
        baseURL: 'https://app.xwork.co/api',
        timeout: 180000
      })

      getToken()
    }
  }
}

function getToken() {
  var payload = new FormData()
  payload.append('grant_type', 'client_credentials')
  payload.append('client_id', 1)
  payload.append('client_secret', 'quZ8CX2thlcgzKlKz0D3_okfPwNUCaZ7WEejCPS3LHPhp4h2sAvBC4zL')

  _axios.post('/v1/client/oauth', payload).then(res => {
    var resp = res.data
    window.localStorage.setItem('token', JSON.stringify({
      clientToken: resp.access_token,
      exp: new Date().getTime() + resp.expires_in
    }))

    window._axios = axios.create({
      baseURL: 'https://app.xwork.co/api',
      timeout: 180000,
      headers: {
        Authorization: 'Bearer ' + resp.access_token
      }
    })

    getBuilding()
    initSearch()
  }).catch(err => {
    alert('Error get token')
    console.error(err)
  })
}

function initMap() {
  window.fullscreenLoading = $('#fullscreen-loading')
  if (!L) {
    return setTimeout(function() {
      return initMap()
    }, 200);
  } else {
    window.map = L.map('xwork-map', {
      center: [-2.2406396093827206, 120.30029296875001],
      zoom: 5
    })
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic2lkaWttYXAiLCJhIjoiY2p2M2o1ZmZuMDlmODQzb2NrN2dvcmVoNyJ9.rWonus9FOQwiPzBK7Mfoaw', {
      attribution: '&copy; <a href="https://www.mapbox.com/">Mapbox</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      id: 'mapbox.streets',
      maxZoom: 18,
      accessToken: 'pk.eyJ1Ijoic2lkaWttYXAiLCJhIjoiY2p2M2o1ZmZuMDlmODQzb2NrN2dvcmVoNyJ9.rWonus9FOQwiPzBK7Mfoaw'
    }).addTo(window.map)
  }
}

function getBuilding(lat, lon) {
  // fullscreenLoading.hide()
  if (!lat) { lat = -2.2406396093827206 }
  if (!lon) { lon = 120.30029296875001 }
  window._axios.get('/v2/rooms/search?results_per_page=10000&radius=10000&lat=' + lat + '&lon=' + lon).then(function (res) {
    var resp = res.data
    parseBuilding(resp)
  }).catch(function (err) {
    alert('Error in fetching building')
    console.error(err)
  })
}

function parseBuilding(data) {
  var markers = L.markerClusterGroup()
  data.buildings.forEach(function (building, index) {
    var buildingsRooms = data.rooms.filter(function (room, idx) {
      return room.id_building === building.id
    })

    var customMarker = document.createElement('div')
    customMarker.classList.add('custom-marker')

    var markerIcon = document.createElement('img')
    markerIcon.setAttribute('src', '/static/map-openlayer/building-icon.png')
    // markerIcon.setAttribute('src', 'building-icon.png')
    markerIcon.setAttribute('lat', building.lat)
    markerIcon.setAttribute('lon', building.lon)

    var roomCount = document.createElement('p')
    roomCount.textContent = buildingsRooms.length + ' ruangan'
    roomCount.classList.add('rooms-count')
    roomCount.setAttribute('lat', building.lat)
    roomCount.setAttribute('lon', building.lon)

    var buildingDetail = document.createElement('div')
    buildingDetail.classList.add('building-detail')

    var buildingNameLink = document.createElement('a')
    buildingNameLink.setAttribute('href', 'https://xwork.co/p/b-' + building.name.toLowerCase().split(' ').join('-') + '-' + building.id)
    buildingNameLink.setAttribute('target', '_blank')

    var buildingName = document.createElement('p')
    buildingName.classList.add('building-name')
    buildingName.textContent = building.name

    buildingNameLink.appendChild(buildingName)

    var buildingDetailTopLink = document.createElement('a')
    buildingDetailTopLink.setAttribute('href', 'https://xwork.co/p/b-' + building.name.toLowerCase().split(' ').join('-') + '-' + building.id)
    buildingDetailTopLink.setAttribute('target', '_blank')

    var buildingDetailTop = document.createElement('div')
    buildingDetailTop.classList.add('top')

    var buildingImage = document.createElement('img')
    buildingImage.setAttribute('src', building.picture)
    buildingImage.setAttribute('onerror', 'this.orerror=null;this.src="/static/map-openlayer/building-error.jpg"')
    // buildingImage.setAttribute('onerror', 'this.orerror=null;this.src="building-error.jpg"')

    var buildingAdress = document.createElement('p')
    buildingAdress.textContent = building.address

    var roomsImageContainer = document.createElement('div')
    roomsImageContainer.classList.add('rooms-container')

    buildingsRooms.forEach(function(room) {
      var imageLink = document.createElement('a')
      imageLink.setAttribute('title', room.name)
      imageLink.setAttribute('href', 'https://xwork.co/room-detail/' + room.type.toLowerCase().split(' ').join('-') + '-di-' + room.name.toLowerCase().split(' ').join('-') + '-' + room.id)
      imageLink.setAttribute('target', '_blank')

      var image = document.createElement('img')
      image.setAttribute('src', room.cimages.url + '/' + room.id + '/' + room.cimages.images[0] + '/' + room.id + '_' + room.cimages.images[0] + '.thumb.' + room.cimages.image_format)

      imageLink.appendChild(image)
      roomsImageContainer.appendChild(imageLink)
    })

    buildingDetailTop.appendChild(buildingImage)
    buildingDetailTop.appendChild(buildingAdress)

    buildingDetailTopLink.appendChild(buildingDetailTop)

    buildingDetail.appendChild(buildingNameLink)
    buildingDetail.appendChild(buildingDetailTopLink)
    buildingDetail.appendChild(roomsImageContainer)

    customMarker.appendChild(markerIcon)
    customMarker.appendChild(roomCount)
    customMarker.appendChild(buildingDetail)

    markers.addLayer(L.marker([building.lat, building.lon], {
      icon: L.divIcon({
        html: customMarker.outerHTML,
        iconSize: [37, 44]
      })
    }))
    if (index === data.buildings.length - 1) {
      window.map.addLayer(markers)
      fullscreenLoading.hide()
      initMarkerClick()
      window.map.on('zoomend moveend', initMarkerClick)
    }
  })
}

function initMarkerClick() {
  $('.custom-marker > img, .custom-marker > p').off('click').click(function (e) {
    var marker = $(e.currentTarget)
    var buildingDetail = marker.parent().find('.building-detail')
    if (buildingDetail.css('display') === 'none') {
      $('.building-detail').hide()
      buildingDetail.show()
    } else {
      buildingDetail.hide()
    }

    window.map.setView([Number(marker.attr('lat')), Number(marker.attr('lon'))])
  })
}

function initSearch() {
  var input = document.getElementById('search-area')

  autocomplete({
    input: input,
    fetch: function(text, update) {
      text = text.toLowerCase()
      _axios.get('/v1/client/meeting_room/autocomplete?query=' + text).then(res => {
        var resp = res.data.data
        console.log(resp)
        var respJoin = resp.buildings.concat(resp.regions)
        var areaList = respJoin.map(function (li) {
          return {
            label: li.name + ', ' + li.additional_info + '    ' + '[' + li.tag.toUpperCase() + ']',
            value: li.id,
            lat: li.lat,
            lon: li.lon,
            zoom: getZoom(li.tag)
          }
        }).sort(function(_a, _b) {
          var a = _a.label.toLowerCase()
          var b = _b.label.toLowerCase()
          var _query = text.toLowerCase()
          if (a === _query) {
            return -1
          } else if (a.split(_query)[0] === '' || b.split(_query)[0] === '') {
            if (b.split(_query)[0] !== '') {
              return -1
            } else if (a.split(_query)[0] !== '') {
              return 1
            } else {
              if (a.replace(_query, '').length < b.replace(_query, '').length) {
                return -1
              } else {
                return 1
              }
            }
          } else if (a.includes(_query)) {
            if (!b.includes(_query)) {
              return -1
            } else {
              if (a.length < b.length) {
                return -1
              } else {
                return 1
              }
            }
          } else {
            return 1
          }
        })
        update(areaList)
        if (!window.initialCummulative) { window.initialCummulative = [] }
        var tagCompilation = respJoin.reduce((a, b) => {
          console.log(a)
          if (a.indexOf(b.tag) === -1) {
            a.push(b.tag)
          }
          return a
        }, window.initialCummulative)
        window.initialCummulative = tagCompilation
        console.log(window.initialCummulative)
      }).catch(err => {
        alert('Error fetching area list')
        console.error(err)
      })
    },
    onSelect: function(item) {
      input.value = item.label
      window.map.setView([item.lat, item.lon], item.zoom)
    }
  });
}

function getZoom(type) {
  // switch (type) {
  //   case 'city':
  //     return 13
  //   case 'village':
  //     return 14
  //   case 'administrative':
  //     return 15
  //   default:
  //     return 16
  // }
  switch (type.toLowerCase()) {
    case 'provinsi':
      return 12
    case 'kota':
      return 13
    default:
      return 16
  }
}