import { useState } from 'react'

export default function LandingPage({ onEnter }) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      background: 'linear-gradient(135deg, #000000 0%, #0a0a0a 50%, #000000 100%)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* Animated background dots */}
      <div style={{
        position: 'absolute',
        width: '100%',
        height: '100%',
        backgroundImage: 'radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px)',
        backgroundSize: '50px 50px',
        animation: 'float 20s ease-in-out infinite',
        opacity: 0.3,
        pointerEvents: 'none',
      }} />
      
      {/* Main content */}
      <div style={{
        zIndex: 10,
        textAlign: 'center',
        padding: '0 40px',
        maxWidth: '800px',
      }}>
        {/* Logo/Title */}
        <div style={{
          fontFamily: 'Bebas Neue',
          fontSize: '6rem',
          letterSpacing: '0.15em',
          color: '#FFFFFF',
          marginBottom: '20px',
          textShadow: '0 0 30px rgba(255,255,255,0.3)',
          lineHeight: 1,
        }}>
          KAIROS
        </div>
        
        {/* Subtitle */}
        <div style={{
          fontFamily: 'JetBrains Mono',
          fontSize: '0.9rem',
          color: '#6B7280',
          letterSpacing: '0.3em',
          marginBottom: '40px',
        }}>
          GLOBAL NEWS INTELLIGENCE
        </div>
        
        {/* Description */}
        <div style={{
          fontFamily: 'DM Sans',
          fontSize: '1.1rem',
          lineHeight: 1.8,
          color: 'rgba(249,250,251,0.8)',
          marginBottom: '60px',
          maxWidth: '600px',
          margin: '0 auto 60px',
        }}>
          <p style={{ marginBottom: '20px' }}>
            Real-time global news intelligence for stock market analysis. 
            World events move markets, and Kairos makes that connection visible. 
            Click any country to see how news is driving financial markets with 
            AI-powered analysis and live market data.
          </p>
          <p style={{ 
            fontSize: '0.95rem',
            color: 'rgba(249,250,251,0.6)',
            fontStyle: 'italic',
          }}>
            Connecting global events to market movements in real time.
          </p>
        </div>
        
        {/* CTA Button */}
        <button
          onClick={onEnter}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          style={{
            fontFamily: 'JetBrains Mono',
            fontSize: '0.9rem',
            letterSpacing: '0.2em',
            color: '#000000',
            background: isHovered ? '#FFFFFF' : 'rgba(255,255,255,0.9)',
            border: '2px solid #FFFFFF',
            padding: '16px 48px',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            boxShadow: isHovered 
              ? '0 0 30px rgba(255,255,255,0.4), 0 8px 16px rgba(0,0,0,0.3)'
              : '0 4px 12px rgba(0,0,0,0.2)',
            transform: isHovered ? 'translateY(-2px)' : 'translateY(0)',
            fontWeight: '600',
          }}
        >
          ENTER GLOBE →
        </button>
      </div>
      
      {/* Footer hint */}
      <div style={{
        position: 'absolute',
        bottom: '40px',
        fontFamily: 'JetBrains Mono',
        fontSize: '0.65rem',
        color: '#6B7280',
        letterSpacing: '0.15em',
        opacity: 0.6,
      }}>
        Click any country marker to begin
      </div>
    </div>
  )
}
