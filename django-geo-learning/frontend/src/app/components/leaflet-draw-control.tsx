'use client'

// src/MapWithDraw.tsx
import 'leaflet-draw/dist/leaflet.draw.css';
import 'leaflet/dist/leaflet.css';
import { useMap } from 'react-leaflet';

import L from 'leaflet';
import 'leaflet-draw';
import React from 'react';

// Adiciona o ícone customizado
const customIcon = new L.Icon({
  iconUrl: '/marker2.webp', // Caminho para o arquivo de imagem (pode ser no diretório public do Next.js)
  iconSize: [64, 64],          // Tamanho do ícone
  iconAnchor: [30, 50],        // O ponto do ícone onde o marcador será ancorado (meia largura e altura)
  popupAnchor: [0, -32],       // O ponto de onde o pop-up será ancorado (relativo ao ícone)
});

export default function LeafletDrawControl() {
  const map = useMap();

  React.useEffect(() => {
    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    const drawControl = new L.Control.Draw({
      draw: {
        polygon: false,
        polyline: false,
        rectangle: false,
        circle: false,
        circlemarker: false,
        marker: {
          icon: customIcon, // Aqui você define o ícone customizado
        },
      },
      edit: {
        featureGroup: drawnItems,
      },
    });

    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, function (event: any) {
      const { layer } = event;
      drawnItems.addLayer(layer);

      if (layer instanceof L.Marker) {
        const { lat, lng } = layer.getLatLng();
        console.log('Ponto criado em:', { lat, lng });
      }
    });

    return () => {
      map.off();
      map.removeControl(drawControl);
    };
  }, [map]);

  return null;
}
