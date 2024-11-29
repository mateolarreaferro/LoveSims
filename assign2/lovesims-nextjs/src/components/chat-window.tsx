import { useEffect, useRef } from 'react';
import { Card } from './ui/card';
import { ScrollArea } from './ui/scroll-area';

interface Message {
  agent: string;
  response: string;
  number: number;
}

interface ChatWindowProps {
  messages: Message[];
  className?: string;
}

export function ChatWindow({ messages, className = '' }: ChatWindowProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Card className={`h-[600px] ${className}`}>
      <ScrollArea ref={scrollRef} className="h-full p-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex flex-col max-w-[80%] ${
                message.number === 0
                  ? 'mx-auto text-center font-semibold'
                  : 'ml-4'
              }`}
            >
              {message.number !== 0 && (
                <span className="text-sm font-medium text-muted-foreground">
                  {message.agent}
                </span>
              )}
              <div
                className={`rounded-lg p-3 ${
                  message.number === 0
                    ? 'bg-muted'
                    : 'bg-primary text-primary-foreground'
                }`}
              >
                {message.number === 0
                  ? message.response
                  : message.response.split(': ')[1]}
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
    </Card>
  );
}
