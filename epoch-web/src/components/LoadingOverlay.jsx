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
      <div style={{
        background: 'rgba(10,15,26,0.95)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(245,158,11,0.2)',
        borderRadius: '12px',
        padding: '24px 32px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '16px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
      }}>
        <div className="spin-slow" style={{
          width: '48px',
          height: '48px',
          border: '3px solid rgba(245,158,11,0.15)',
          borderTop: '3px solid #F59E0B',
          borderRadius: '50%',
        }} />
        <div style={{
          fontFamily: 'JetBrains Mono',
          fontSize: '0.7rem',
          color: '#F59E0B',
          letterSpacing: '0.2em',
          textAlign: 'center',
        }}>
          RETRIEVING SIGNAL...
        </div>
        <div style={{
          fontFamily: 'DM Sans',
          fontSize: '0.65rem',
          color: '#6B7280',
          letterSpacing: '0.05em',
          textAlign: 'center',
          marginTop: '-4px',
        }}>
          Fetching news • Generating summary • Creating audio
        </div>
      </div>
    </div>
  )
}
