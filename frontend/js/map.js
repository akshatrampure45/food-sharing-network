let map, marker;

function initMap(lat = 18.5204, lng = 73.8567) {
  map = L.map("map").setView([lat, lng], 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);
  return map;
}

// Click-to-drop-pin, used on the donate page to set a listing's location
function enablePinDrop(onPick) {
  map.on("click", (e) => {
    const { lat, lng } = e.latlng;
    if (marker) map.removeLayer(marker);
    marker = L.marker([lat, lng]).addTo(map);
    onPick(lat, lng);
  });
}

function plotListings(listings) {
  listings.forEach((l) => {
    L.marker([l.lat, l.lng])
      .addTo(map)
      .bindPopup(`<strong>${l.title}</strong><br>${l.quantity}<br>Freshness: ${l.freshness_score ?? "n/a"}`);
  });
}
