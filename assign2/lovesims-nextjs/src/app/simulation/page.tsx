'use client';

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Users, User, UsersRound } from "lucide-react"
import Link from "next/link"

export default function SimulationPage() {
  return (
    <main className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="space-y-8">
        <div className="flex items-center gap-4">
          <Link href="/">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="h-4 w-4" />
            </Button>
          </Link>
          <h1 className="text-3xl font-bold tracking-tight">Choose Simulation Mode</h1>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          <Link href="/simulation/one-to-one" className="block">
            <Card className="h-full hover:bg-accent transition-colors cursor-pointer">
              <CardHeader>
                <Users className="h-8 w-8 mb-2" />
                <CardTitle>One-to-One</CardTitle>
                <CardDescription>
                  Simulate a date between two specific agents
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Perfect for exploring specific personality combinations or practicing 
                  particular dating scenarios.
                </p>
              </CardContent>
            </Card>
          </Link>

          <Link href="/simulation/one-to-all" className="block">
            <Card className="h-full hover:bg-accent transition-colors cursor-pointer">
              <CardHeader>
                <User className="h-8 w-8 mb-2" />
                <CardTitle>One-to-All</CardTitle>
                <CardDescription>
                  One agent dates all other agents
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  See how one personality type interacts with different kinds of people. 
                  Great for understanding compatibility patterns.
                </p>
              </CardContent>
            </Card>
          </Link>

          <Link href="/simulation/all-pairs" className="block">
            <Card className="h-full hover:bg-accent transition-colors cursor-pointer">
              <CardHeader>
                <UsersRound className="h-8 w-8 mb-2" />
                <CardTitle>All Pairs</CardTitle>
                <CardDescription>
                  Simulate dates between all possible pairs
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Run a comprehensive simulation of all possible agent combinations. 
                  Ideal for analyzing overall dating dynamics.
                </p>
              </CardContent>
            </Card>
          </Link>
        </div>
      </div>
    </main>
  )
}
