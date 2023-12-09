import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup, useMap, ImageOverlay, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import IMAGE from './map.png';
import L from 'leaflet';
import robotImage from './robot.jpeg';
import Button from 'react-bootstrap/Button';
import '@coreui/coreui/dist/css/coreui.min.css';
import { CButton } from '@coreui/react';

const Dashboard = () => {
  const [coordinates, setCoordinates] = useState({ x: 0, y: 0, theta: 0 });
  const [path, setPath] = useState([]);
  const initializedRef = useRef(false);
  const textureRef = useRef();
  const [mission, setCurrentMission] = useState();

  const RobotMarker = () => {
    const map = useMap();

    const customIcon = new L.Icon({
      iconUrl: robotImage,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
      popupAnchor: [0, -16],
    });

    const leafletCoords = map.latLngToLayerPoint([coordinates.y, coordinates.x]);

    return (
      <Marker position={map.layerPointToLatLng(leafletCoords)} icon={customIcon}>
        <Popup>{coordinates.x}, {coordinates.y}</Popup>
      </Marker>
    );
  };

  useEffect(() => {
    // Update the path with the new coordinates
    if (coordinates.x !== 0 && coordinates.y !== 0) {
      setPath((prevPath) => [...prevPath, [coordinates.y, coordinates.x]]);
    }
  }, [coordinates]);

  const handleMissionClick = (missionNumber) => {
    setCurrentMission(missionNumber);

    // Clear the path when starting a new mission
    setPath([]);

    axios
      .post('http://localhost:8000/add-mission/', { missionNumber })
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

    const socket = new WebSocket(`ws://localhost:8765/${missionNumber}`);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setCoordinates(data);
    };
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <div style={{ flex: 1, position: 'relative' }}>
        <MapContainer center={[0, 0]} zoom={2} style={{ height: '100%', width: '100%' }}>
          <ImageOverlay
            url={IMAGE}
            bounds={[
              [-90, -180],
              [90, 180],
            ]}
          />
          {coordinates && <RobotMarker />}
          {path.length > 1 && <Polyline positions={path} color="blue" />}
        </MapContainer>
      </div>
      <div style={{ textAlign: 'left', padding: '10px' }}>
        <CButton color="primary" onClick={() => handleMissionClick(1)} style={{ marginRight: '10px' }}>
          Mission 1
        </CButton>
        <CButton color="primary" onClick={() => handleMissionClick(2)} style={{ marginRight: '10px' }}>
          Mission 2
        </CButton>
        <CButton color="primary" onClick={() => handleMissionClick(3)}>
          Mission 3
        </CButton>
        <p style={{ fontFamily: 'Arial', marginTop: '10px' }}>Current State of Robot: {JSON.stringify(coordinates)}</p>
      </div>
    </div>
  );
};

export default Dashboard;
