import { useEffect, useRef, useState } from 'react'

export default function CountryPanel({ data, onClose }) {
  const audioRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)

  useEffect(() => {
    if (!data?.audio_base64) return
    
    const audio = new Audio(`data:audio/mpeg;base64,${data.audio_base64}`)
    audioRef.current = audio
    audio.onplay = () => setIsPlaying(true)
    audio.onended = () => setIsPlaying(false)
    audio.onpause = () => setIsPlaying(false)
    
    // Auto-play audio on mount
    audio.play().catch((e) => {
      console.error('Audio play failed:', e)
    })
    
    return () => {
      if (audioRef.current) {
        audioRef.current.pause()
        audioRef.current = null
      }
    }
  }, [data])

  const toggleAudio = () => {
    if (!audioRef.current) return
    if (isPlaying) {
      audioRef.current.pause()
    } else {
      audioRef.current.currentTime = 0
      audioRef.current.play()
    }
  }

  return (
    <div className="slide-in" style={{
      position: 'absolute',
      top: 0,
      right: 0,
      width: '420px',
      height: '100vh',
      background: 'rgba(10,15,26,0.92)',
      backdropFilter: 'blur(20px)',
      borderLeft: '1px solid rgba(255,255,255,0.08)',
      zIndex: 20,
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        padding: '28px 28px 20px',
        borderBottom: '1px solid rgba(255,255,255,0.06)',
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'space-between',
      }}>
        <div>
          <div style={{
            fontFamily: 'JetBrains Mono',
            fontSize: '0.6rem',
            color: '#F59E0B',
            letterSpacing: '0.2em',
            marginBottom: '6px',
          }}>
            LIVE BRIEFING
          </div>
          <div style={{
            fontFamily: 'Bebas Neue',
            fontSize: '2.2rem',
            letterSpacing: '0.05em',
            color: '#F9FAFB',
            lineHeight: 1,
          }}>
            {data.country.toUpperCase()}
          </div>
        </div>
        <button
          onClick={onClose}
          style={{
            background: 'rgba(255,255,255,0.05)',
            border: '1px solid rgba(255,255,255,0.1)',
            color: '#6B7280',
            width: '32px',
            height: '32px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '1rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
          }}
        >
          ✕
        </button>
      </div>

      {/* Audio Player */}
      <div style={{
        margin: '16px 28px',
        padding: '14px 18px',
        background: 'rgba(245,158,11,0.08)',
        border: '1px solid rgba(245,158,11,0.2)',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        gap: '14px',
        cursor: 'pointer',
      }} onClick={toggleAudio}>
        {/* ON AIR indicator */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexShrink: 0 }}>
          <div className={isPlaying ? 'pulse-dot' : ''} style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: isPlaying ? '#EF4444' : '#6B7280',
          }} />
          <span style={{
            fontFamily: 'JetBrains Mono',
            fontSize: '0.6rem',
            letterSpacing: '0.15em',
            color: isPlaying ? '#EF4444' : '#6B7280',
          }}>
            {isPlaying ? 'ON AIR' : 'PLAY'}
          </span>
        </div>

        {/* Waveform bars (decorative) */}
        <div style={{ display: 'flex', gap: '2px', alignItems: 'center', flex: 1 }}>
          {[...Array(20)].map((_, i) => (
            <div key={i} style={{
              width: '2px',
              height: `${isPlaying ? Math.random() * 16 + 4 : 4}px`,
              background: isPlaying ? '#F59E0B' : 'rgba(245,158,11,0.3)',
              borderRadius: '1px',
              transition: 'height 0.1s ease',
            }} />
          ))}
        </div>

        <span style={{
          fontFamily: 'JetBrains Mono',
          fontSize: '0.65rem',
          color: '#F59E0B',
          flexShrink: 0,
        }}>
          {isPlaying ? '⏸' : '▶'}
        </span>
      </div>

      {/* Summary */}
      <div style={{ padding: '0 28px 20px' }}>
        <div style={{
          fontFamily: 'DM Sans',
          fontSize: '0.9rem',
          lineHeight: 1.7,
          color: 'rgba(249,250,251,0.8)',
        }}>
          {data.summary}
        </div>
      </div>

      {/* Headlines */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '0 28px 28px',
      }}>
        <div style={{
          fontFamily: 'JetBrains Mono',
          fontSize: '0.6rem',
          color: '#6B7280',
          letterSpacing: '0.2em',
          marginBottom: '12px',
        }}>
          LATEST HEADLINES
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {data.headlines.map((headline, i) => {
            const headlineText = typeof headline === 'string' ? headline : headline.title || headline
            const headlineUrl = typeof headline === 'object' ? headline.url : null
            
            return (
              <div key={i} style={{
                padding: '12px 14px',
                background: 'rgba(255,255,255,0.03)',
                border: '1px solid rgba(255,255,255,0.06)',
                borderRadius: '6px',
                display: 'flex',
                gap: '12px',
                alignItems: 'flex-start',
                transition: 'all 0.2s ease',
                cursor: headlineUrl ? 'pointer' : 'default',
              }}
              onClick={() => {
                if (headlineUrl) {
                  window.open(headlineUrl, '_blank', 'noopener,noreferrer')
                }
              }}
              onMouseEnter={(e) => {
                if (headlineUrl) {
                  e.currentTarget.style.background = 'rgba(255,255,255,0.06)'
                  e.currentTarget.style.borderColor = 'rgba(245,158,11,0.3)'
                }
              }}
              onMouseLeave={(e) => {
                if (headlineUrl) {
                  e.currentTarget.style.background = 'rgba(255,255,255,0.03)'
                  e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)'
                }
              }}
              >
                <span style={{
                  fontFamily: 'JetBrains Mono',
                  fontSize: '0.6rem',
                  color: '#F59E0B',
                  flexShrink: 0,
                  marginTop: '2px',
                }}>
                  {String(i + 1).padStart(2, '0')}
                </span>
                <div style={{ flex: 1 }}>
                  <span style={{
                    fontFamily: 'DM Sans',
                    fontSize: '0.82rem',
                    lineHeight: 1.5,
                    color: headlineUrl ? 'rgba(245,158,11,0.9)' : 'rgba(249,250,251,0.75)',
                    textDecoration: headlineUrl ? 'underline' : 'none',
                    textUnderlineOffset: '2px',
                  }}>
                    {headlineText}
                  </span>
                  {headlineUrl && (
                    <div style={{
                      fontFamily: 'JetBrains Mono',
                      fontSize: '0.55rem',
                      color: '#6B7280',
                      marginTop: '4px',
                      opacity: 0.7,
                    }}>
                      Click to read →
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
