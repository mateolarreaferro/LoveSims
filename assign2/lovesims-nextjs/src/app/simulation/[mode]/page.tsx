'use client';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { ChatWindow } from '@/components/chat-window';
import { agentList } from '@/lib/constants';
import { useState, useEffect } from 'react';
import { startDates, createEventSource, runDates, resetGame } from '@/lib/api';
import { useParams } from 'next/navigation';

const DURATION_OPTIONS = [
  { value: '6', label: '6 responses' },
  { value: '10', label: '10 responses' },
  { value: '16', label: '16 responses' },
];

export default function SimulationModePage() {
  const params = useParams();
  const mode = params.mode as string;
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [dateContext, setDateContext] = useState('');
  const [duration, setDuration] = useState('10');
  const [messages, setMessages] = useState<any[]>([]);
  const [isRunning, setIsRunning] = useState(false);

  const modeTitles = {
    'one-to-one': 'One-to-One Simulation',
    'one-to-all': 'One-to-All Simulation',
    'all-pairs': 'All Pairs Simulation',
  };

  useEffect(() => {
    // Reset game when component unmounts
    return () => {
      resetGame();
    };
  }, []);

  const handleStartSimulation = async () => {
    try {
      setMessages([]);
      setIsRunning(true);

      // Initialize the simulation
      await startDates({
        mode,
        agents: selectedAgents,
        dateContext: mode !== 'all-pairs' ? dateContext : undefined,
        dateDuration: parseInt(duration),
      });

      // Set up event source for streaming responses
      const eventSource = createEventSource();
      
      eventSource.onmessage = (event) => {
        const messageData = JSON.parse(event.data);
        setMessages((prev) => [...prev, messageData]);
      };

      eventSource.onerror = (error) => {
        console.error('EventSource failed:', error);
        eventSource.close();
        setIsRunning(false);
      };

      // Start running the dates
      const response = await runDates();
      
      if (response.status === 'completed') {
        setTimeout(() => {
          eventSource.close();
          setIsRunning(false);
        }, 1000);
      }
    } catch (error) {
      console.error('Error running simulation:', error);
      setIsRunning(false);
    }
  };

  return (
    <main className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="space-y-8">
        <div className="flex items-center gap-4">
          <Link href="/simulation">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="h-4 w-4" />
            </Button>
          </Link>
          <h1 className="text-3xl font-bold tracking-tight">{modeTitles[mode as keyof typeof modeTitles]}</h1>
        </div>

        <div className="grid gap-6 md:grid-cols-[350px_1fr]">
          <Card>
            <CardHeader>
              <CardTitle>Simulation Settings</CardTitle>
              <CardDescription>Configure your dating simulation</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {mode === 'one-to-one' && (
                <>
                  <div className="space-y-2">
                    <Label>First Agent</Label>
                    <Select
                      value={selectedAgents[0]}
                      onValueChange={(value) =>
                        setSelectedAgents([value, selectedAgents[1] || ''])
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select first agent" />
                      </SelectTrigger>
                      <SelectContent>
                        {agentList.map((agent) => (
                          <SelectItem key={agent} value={agent}>
                            {agent}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Second Agent</Label>
                    <Select
                      value={selectedAgents[1]}
                      onValueChange={(value) =>
                        setSelectedAgents([selectedAgents[0] || '', value])
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select second agent" />
                      </SelectTrigger>
                      <SelectContent>
                        {agentList.map((agent) => (
                          <SelectItem key={agent} value={agent}>
                            {agent}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </>
              )}

              {mode === 'one-to-all' && (
                <div className="space-y-2">
                  <Label>Select Agent</Label>
                  <Select
                    value={selectedAgents[0]}
                    onValueChange={(value) => setSelectedAgents([value])}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select an agent" />
                    </SelectTrigger>
                    <SelectContent>
                      {agentList.map((agent) => (
                        <SelectItem key={agent} value={agent}>
                          {agent}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}

              {mode !== 'all-pairs' && (
                <div className="space-y-2">
                  <Label>Date Context</Label>
                  <Textarea
                    value={dateContext}
                    onChange={(e) => setDateContext(e.target.value)}
                    placeholder="Describe the date context..."
                    rows={3}
                  />
                </div>
              )}

              <div className="space-y-2">
                <Label>Responses per Date</Label>
                <Select value={duration} onValueChange={setDuration}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {DURATION_OPTIONS.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
            <CardFooter>
              <Button
                className="w-full"
                onClick={handleStartSimulation}
                disabled={
                  isRunning ||
                  (mode === 'one-to-one' && (!selectedAgents[0] || !selectedAgents[1])) ||
                  (mode === 'one-to-all' && !selectedAgents[0]) ||
                  (mode !== 'all-pairs' && !dateContext)
                }
              >
                {isRunning ? 'Running Simulation...' : 'Start Simulation'}
              </Button>
            </CardFooter>
          </Card>

          <ChatWindow messages={messages} />
        </div>
      </div>
    </main>
  );
}
