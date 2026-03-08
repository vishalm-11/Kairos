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
    <>
      {/* Backdrop overlay - clickable to close */}
      <div 
        onClick={onClose}
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.5)',
          backdropFilter: 'blur(4px)',
          zIndex: 19,
        }}
      />
      
      {/* Centered semi-transparent overlay */}
      <div className="fade-in" style={{
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '600px',
        maxWidth: '90vw',
        maxHeight: '85vh',
        background: 'rgba(0,0,0,0.75)',
        backdropFilter: 'blur(20px) saturate(180%)',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '16px',
        boxShadow: '0 20px 60px rgba(0,0,0,0.8)',
        zIndex: 20,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}>
        {/* Header */}
        <div style={{
          padding: '28px 28px 20px',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          flexShrink: 0,
        }}>
          <div>
            <div style={{
              fontFamily: 'JetBrains Mono',
              fontSize: '0.6rem',
              color: '#FFFFFF',
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
              background: 'rgba(255,255,255,0.08)',
              border: '1px solid rgba(255,255,255,0.15)',
              color: '#FFFFFF',
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '1.1rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.15)'
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.25)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.08)'
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.15)'
            }}
          >
            ✕
          </button>
        </div>

        {/* Audio Player */}
        <div style={{
          margin: '16px 28px',
          padding: '14px 18px',
          background: 'rgba(255,255,255,0.08)',
          border: '1px solid rgba(255,255,255,0.15)',
          borderRadius: '8px',
          display: 'flex',
          alignItems: 'center',
          gap: '14px',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
        }} 
        onClick={toggleAudio}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = 'rgba(255,255,255,0.12)'
          e.currentTarget.style.borderColor = 'rgba(255,255,255,0.25)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'rgba(255,255,255,0.08)'
          e.currentTarget.style.borderColor = 'rgba(255,255,255,0.15)'
        }}
        >
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
                background: isPlaying ? '#FFFFFF' : 'rgba(255,255,255,0.3)',
                borderRadius: '1px',
                transition: 'height 0.1s ease',
              }} />
            ))}
          </div>

          <span style={{
            fontFamily: 'JetBrains Mono',
            fontSize: '0.65rem',
            color: '#FFFFFF',
            flexShrink: 0,
          }}>
            {isPlaying ? '⏸' : '▶'}
          </span>
        </div>

        {/* Scrollable Content Container */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
        }}>
          {/* Summary */}
          <div style={{ padding: '0 28px 20px' }}>
            <div style={{
              fontFamily: 'DM Sans',
              fontSize: '0.95rem',
              lineHeight: 1.75,
              color: 'rgba(249,250,251,0.95)',
              fontWeight: '400',
            }}>
              {data.summary}
            </div>
          </div>

          {/* Economic Pulse */}
          {data.economics && (data.economics.currency || data.economics.stock) && (
            <div style={{
              margin: '0 28px 20px',
              padding: '14px 16px',
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(255,255,255,0.06)',
              borderRadius: '8px',
            }}>
              <div style={{
                fontFamily: 'JetBrains Mono',
                fontSize: '0.6rem',
                color: '#6B7280',
                letterSpacing: '0.2em',
                marginBottom: '10px',
              }}>
                ECONOMIC PULSE
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {data.economics.currency_code !== "USD" && data.economics.currency && data.economics.currency.formatted && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontFamily: 'DM Sans', fontSize: '0.8rem', color: '#6B7280' }}>
                      Currency
                    </span>
                    <span style={{ fontFamily: 'JetBrains Mono', fontSize: '0.75rem', color: '#F9FAFB' }}>
                      {data.economics.currency.formatted}
                    </span>
                  </div>
                )}
                {data.economics.stock && data.economics.stock.formatted && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontFamily: 'DM Sans', fontSize: '0.8rem', color: '#6B7280' }}>
                      Markets
                    </span>
                    <span style={{
                      fontFamily: 'JetBrains Mono',
                      fontSize: '0.75rem',
                      color: data.economics.stock.direction === 'up' ? '#44FF88' : '#EF4444',
                    }}>
                      {data.economics.stock.formatted}
                    </span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Headlines */}
          <div style={{
            padding: '0 28px 28px',
          }}>
            <div style={{
              fontFamily: 'JetBrains Mono',
              fontSize: '0.65rem',
              color: 'rgba(255,255,255,0.5)',
              letterSpacing: '0.25em',
              marginBottom: '16px',
              fontWeight: '500',
            }}>
              LATEST HEADLINES
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {data.headlines && data.headlines.length > 0 ? (
                data.headlines.map((headline, i) => {
                  const headlineText = typeof headline === 'string' ? headline : (headline?.title || headline || '')
                  const headlineUrl = typeof headline === 'object' && headline ? headline.url : null
                
                return (
                  <div key={i} style={{
                    padding: '14px 16px',
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid rgba(255,255,255,0.08)',
                    borderRadius: '10px',
                    display: 'flex',
                    gap: '14px',
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
                      e.currentTarget.style.background = 'rgba(255,255,255,0.08)'
                      e.currentTarget.style.borderColor = 'rgba(255,255,255,0.2)'
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (headlineUrl) {
                      e.currentTarget.style.background = 'rgba(255,255,255,0.03)'
                      e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'
                    }
                  }}
                  >
                    <span style={{
                      fontFamily: 'JetBrains Mono',
                      fontSize: '0.6rem',
                      color: '#FFFFFF',
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
                        color: headlineUrl ? '#FFFFFF' : 'rgba(249,250,251,0.75)',
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
                })
              ) : (
                <div style={{
                  padding: '14px 16px',
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: '10px',
                  fontFamily: 'DM Sans',
                  fontSize: '0.82rem',
                  color: 'rgba(249,250,251,0.75)',
                }}>
                  No headlines available at this time.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
