export default function LoadingOverlay() {
  return (
    <div style={{
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      zIndex: 15,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '14px',
    }}>
      <div className="spin-slow" style={{
        width: '40px',
        height: '40px',
        border: '2px solid rgba(245,158,11,0.15)',
        borderTop: '2px solid #F59E0B',
        borderRadius: '50%',
      }} />
      <div style={{
        fontFamily: 'JetBrains Mono',
        fontSize: '0.65rem',
        color: '#F59E0B',
        letterSpacing: '0.2em',
      }}>
        RETRIEVING SIGNAL...
      </div>
    </div>
  )
}
