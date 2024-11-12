import { useState, useEffect } from 'react'
import '../assets/styles/chat.css'

export default function ChatIA() {
  const [isOpen, setIsOpen] = useState(false)
  const [showFloatingMessage, setShowFloatingMessage] = useState(false)
  const [messages, setMessages] = useState<{ text: string; sender: 'user' | 'ai' }[]>([
    { text: "¡Boo! No temas, soy tu guía espeluznante en esta plataforma de películas de terror. Pregúntame lo que quieras sobre la plataforma o sobre películas escalofriantes. ¡Estoy muriendo por ayudarte!", sender: 'ai' }
  ])
  const [input, setInput] = useState('')

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowFloatingMessage(true)
    }, 3000)

    return () => clearTimeout(timer)
  }, [])

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }])
      setInput('')
      // Aquí puedes agregar la lógica para procesar la pregunta del usuario y generar una respuesta
    }
  }

  return (
    <div className="chat-container">
      {!isOpen && (
        <>
          <button 
            onClick={() => setIsOpen(true)} 
            className="chat-button"
            onMouseEnter={() => setShowFloatingMessage(true)}
            onMouseLeave={() => setShowFloatingMessage(false)}
          >
            🦇
          </button>
          {showFloatingMessage && (
            <div className="floating-message">
              ¿Necesitas ayuda espeluznante? ¡Haz clic aquí!
            </div>
          )}
        </>
      )}
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <span>Chat PeliSoft</span>
            <button onClick={() => setIsOpen(false)} className="close-button">
              X
            </button>
          </div>
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.sender === 'ai' ? 'ai-message' : 'user-message'}`}
              >
                {msg.text}
              </div>
            ))}
          </div>
          <div className="input-area">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Escribe tu pregunta aquí..."
              className="chat-input"
            />
            <button onClick={handleSend} className="send-button">
              Enviar
            </button>
          </div>
        </div>
      )}
    </div>
  )
}