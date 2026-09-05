import { useEffect, useRef, useState } from 'react';
import SiteHeader from './SiteHeader.jsx';

const GREETING =
  "hey — this is a from-scratch chat shell with no assistant wired up. type something and I'll reply with a canned line.";

const CANNED_REPLIES = [
  'still just a mockup — no real brain wired up in here yet.',
  "that's a great question for the real pao-gpt. this one only knows how to nod.",
  "noted. filed under 'things a chatbot would say.'",
  "i'm a placeholder response, but I appreciate the enthusiasm.",
  'beep boop. that is the extent of my intelligence right now.',
  "ask me anything — i'll answer with equally generic confidence.",
  'this reply was picked at random from a list of eight. congrats.',
  'no api, no model, just vibes and a setTimeout.',
];

// The one measurement that reflects the real visible area once a mobile
// keyboard opens: window.innerHeight / 100dvh don't shrink on iOS Safari
// when the keyboard appears, but visualViewport.height does everywhere.
function useVisualViewportHeight() {
  const [height, setHeight] = useState(
    () => window.visualViewport?.height ?? window.innerHeight,
  );

  useEffect(() => {
    const vv = window.visualViewport;
    if (!vv) return;
    const update = () => setHeight(vv.height);
    update();
    vv.addEventListener('resize', update);
    vv.addEventListener('scroll', update);
    return () => {
      vv.removeEventListener('resize', update);
      vv.removeEventListener('scroll', update);
    };
  }, []);

  return height;
}

let nextId = 0;
const makeMessage = (role, text) => ({ id: ++nextId, role, text });

function focusIfFinePointer(ref) {
  const isCoarsePointer = window.matchMedia?.('(pointer: coarse)').matches;
  if (!isCoarsePointer) ref.current?.focus();
}

export default function ChatLab() {
  const [messages, setMessages] = useState(() => [makeMessage('assistant', GREETING)]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const paperRef = useRef(null);
  const inputRef = useRef(null);
  const timeoutRef = useRef(null);
  const vh = useVisualViewportHeight();

  useEffect(() => {
    paperRef.current?.scrollTo({ top: paperRef.current.scrollHeight });
  }, [messages, isTyping, vh]);

  useEffect(() => {
    focusIfFinePointer(inputRef);
    return () => clearTimeout(timeoutRef.current);
  }, []);

  const send = (text) => {
    const trimmed = text.trim();
    if (!trimmed || isTyping) return;
    setMessages((m) => [...m, makeMessage('user', trimmed)]);
    setInput('');
    setIsTyping(true);
    const delay = 450 + Math.random() * 550;
    timeoutRef.current = setTimeout(() => {
      const reply = CANNED_REPLIES[Math.floor(Math.random() * CANNED_REPLIES.length)];
      setMessages((m) => [...m, makeMessage('assistant', reply)]);
      setIsTyping(false);
    }, delay);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    send(input);
  };

  const handleRestart = () => {
    clearTimeout(timeoutRef.current);
    setIsTyping(false);
    setInput('');
    setMessages([makeMessage('assistant', GREETING)]);
    focusIfFinePointer(inputRef);
  };

  return (
    <div className="lab-app" style={vh ? { height: `${vh}px` } : undefined}>
      <SiteHeader />

      <div className="lab-shell">
        <div className="chat-hdr">
          <span className="chat-hdr-mark">pao-gpt</span>
          <button
            className="chat-hdr-restart"
            onClick={handleRestart}
            aria-label="Start a new conversation"
          >
            ↺ restart
          </button>
        </div>

        <div className="lab-paper" ref={paperRef}>
          <div className="lab-msgs">
            {messages.map((m) => (
              <div key={m.id} className={`lab-msg ${m.role}`}>
                <span className="from">{m.role === 'user' ? 'you' : 'bot'}</span>
                <div className="bubble">{m.text}</div>
              </div>
            ))}
            {isTyping && (
              <div className="lab-msg assistant">
                <span className="from">bot</span>
                <div className="bubble typing">
                  typing<span className="typing-caret">▌</span>
                </div>
              </div>
            )}
          </div>
        </div>

        <form className="lab-input" onSubmit={handleSubmit}>
          <div className="field">
            <span className="caret">▌</span>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="type a message…"
              enterKeyHint="send"
              autoComplete="off"
            />
          </div>
          <button type="submit" className="send" disabled={!input.trim()}>
            send <span className="send-glyph">↵</span>
          </button>
        </form>
      </div>
    </div>
  );
}
