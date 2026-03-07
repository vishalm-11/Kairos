import { useEffect, useRef } from 'react'

export default function Globe({ onCountryClick }) {
  const containerRef = useRef(null)
  const viewerRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current || viewerRef.current) return

    const initCesium = async () => {
      const Cesium = await import('cesium')
      await import('cesium/Build/Cesium/Widgets/widgets.css')

      Cesium.Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_TOKEN

      const viewer = new Cesium.Viewer(containerRef.current, {
        timeline: false,
        animation: false,
        baseLayerPicker: false,
        geocoder: false,
        homeButton: false,
        sceneModePicker: false,
        navigationHelpButton: false,
        fullscreenButton: false,
        infoBox: false,
        selectionIndicator: false,
      })

      viewerRef.current = viewer

      viewer.scene.globe.enableLighting = false
      viewer.scene.backgroundColor = Cesium.Color.fromCssColorString('#030712')

      viewer.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(20, 20, 25000000),
      })

      const COUNTRY_CENTROIDS = {
        "United States": [37.0902, -95.7129],
        "Russia": [61.5240, 105.3188],
        "China": [35.8617, 104.1954],
        "India": [20.5937, 78.9629],
        "Brazil": [-14.2350, -51.9253],
        "Ukraine": [48.3794, 31.1656],
        "Iran": [32.4279, 53.6880],
        "Israel": [31.0461, 34.8516],
        "Syria": [34.8021, 38.9968],
        "Yemen": [15.5527, 48.5164],
        "Sudan": [12.8628, 30.2176],
        "Nigeria": [9.0820, 8.6753],
        "Pakistan": [30.3753, 69.3451],
        "Afghanistan": [33.9391, 67.7100],
        "North Korea": [40.3399, 127.5101],
        "Mexico": [23.6345, -102.5528],
        "Germany": [51.1657, 10.4515],
        "France": [46.2276, 2.2137],
        "United Kingdom": [55.3781, -3.4360],
        "Turkey": [38.9637, 35.2433],
        "Saudi Arabia": [23.8859, 45.0792],
        "Egypt": [26.8206, 30.8025],
        "South Africa": [-30.5595, 22.9375],
        "Australia": [-25.2744, 133.7751],
        "Japan": [36.2048, 138.2529],
        "South Korea": [35.9078, 127.7669],
        "Canada": [56.1304, -106.3468],
        "Argentina": [-38.4161, -63.6167],
        "Colombia": [4.5709, -74.2973],
        "Venezuela": [6.4238, -66.5897],
        "Ethiopia": [9.1450, 40.4897],
        "Kenya": [-0.0236, 37.9062],
        "Somalia": [5.1521, 46.1996],
        "Libya": [26.3351, 17.2283],
        "Iraq": [33.2232, 43.6793],
        "Palestine": [31.9522, 35.2332],
        "Taiwan": [23.6978, 120.9605],
        "Myanmar": [21.9162, 95.9560],
        "Philippines": [12.8797, 121.7740],
        "Indonesia": [-0.7893, 113.9213],
      }

      Object.entries(COUNTRY_CENTROIDS).forEach(([name, [lat, lng]]) => {
        viewer.entities.add({
          position: Cesium.Cartesian3.fromDegrees(lng, lat),
          point: {
            pixelSize: 6,
            color: Cesium.Color.fromCssColorString('#F59E0B').withAlpha(0.9),
            outlineColor: Cesium.Color.fromCssColorString('#F59E0B').withAlpha(0.3),
            outlineWidth: 6,
            disableDepthTestDistance: Number.POSITIVE_INFINITY,
          },
          name: name,
        })
      })

      const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas)
      handler.setInputAction((click) => {
        const cartesian = viewer.camera.pickEllipsoid(
          click.position,
          viewer.scene.globe.ellipsoid
        )
        if (!cartesian) return

        const cartographic = Cesium.Cartographic.fromCartesian(cartesian)
        const clickLat = Cesium.Math.toDegrees(cartographic.latitude)
        const clickLng = Cesium.Math.toDegrees(cartographic.longitude)

        let nearest = null
        let minDist = Infinity
        Object.entries(COUNTRY_CENTROIDS).forEach(([name, [lat, lng]]) => {
          const dist = Math.sqrt(
            Math.pow(clickLat - lat, 2) + Math.pow(clickLng - lng, 2)
          )
          if (dist < minDist) {
            minDist = dist
            nearest = name
          }
        })

        if (nearest && minDist < 25) {
          const [lat, lng] = COUNTRY_CENTROIDS[nearest]
          viewer.camera.flyTo({
            destination: Cesium.Cartesian3.fromDegrees(lng, lat, 8000000),
            duration: 1.5,
          })
          onCountryClick(nearest)
        }
      }, Cesium.ScreenSpaceEventType.LEFT_CLICK)
    }

    initCesium().catch(console.error)

    return () => {
      if (viewerRef.current && !viewerRef.current.isDestroyed()) {
        viewerRef.current.destroy()
        viewerRef.current = null
      }
    }
  }, [])

  return (
    <div
      ref={containerRef}
      style={{
        width: '100vw',
        height: '100vh',
        position: 'absolute',
        top: 0,
        left: 0,
        zIndex: 1,
      }}
    />
  )
}