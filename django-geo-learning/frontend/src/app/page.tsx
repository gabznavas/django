'use client'

// src/MapWithDraw.tsx
import 'leaflet-draw/dist/leaflet.draw.css';
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer } from 'react-leaflet';

import 'leaflet-draw';
import LeafletDrawControl from './components/leaflet-draw-control';


export default function MapWithDraw() {
  return (
    <MapContainer
      center={[-22.121265, -51.383400]}
      zoom={15}
      style={{ height: '100vh', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <LeafletDrawControl />
    </MapContainer>
  );
}
