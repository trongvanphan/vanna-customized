/**
 * Home page - Question asking interface
 * Main page for natural language database queries
 */

'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { QuestionInput } from '@/components/QuestionInput';
import { QuestionAnswerCard } from '@/components/QuestionAnswerCard';
import { DarkModeToggle } from '@/components/DarkModeToggle';
import { useAskQuestion } from '@/hooks/useQuery';
import { useToast } from '@/hooks/use-toast';
import { generateId } from '@/lib/utils';
import type { QueryResult } from '@/lib/types';

interface QuestionAnswer {
  id: string;
  question: string;
  result: QueryResult;
  timestamp: Date;
}

export default function Home() {
  const [questionAnswers, setQuestionAnswers] = useState<QuestionAnswer[]>([]);
  const { mutate: askQuestion, isPending } = useAskQuestion();
  const { toast } = useToast();

  const handleSubmit = (question: string, sessionId: string) => {
    askQuestion(
      { question, sessionId },
      {
        onSuccess: (data) => {
          const result: QueryResult = {
            sql: data.sql,
            status: data.error ? 'error' : 'success',
            data: data.data,
            columnNames: data.columns,
            dtypes: data.dtypes,
            error: data.error,
            executionTime: data.execution_time,
            figure_id: data.figure_id,
          };

          const qa: QuestionAnswer = {
            id: generateId(),
            question,
            result,
            timestamp: new Date(),
          };

          // Add to beginning of list
          setQuestionAnswers((prev) => [qa, ...prev]);

          if (result.status === 'success') {
            toast({
              title: 'Query executed successfully',
              description: `Returned ${data.data?.length || 0} rows`,
            });
          }
        },
        onError: (error: unknown) => {
          const errorMessage = 
            (error && typeof error === 'object' && 'error' in error ? String(error.error) : null) ||
            (error instanceof Error ? error.message : null) ||
            'Failed to execute query';
          
          const result: QueryResult = {
            sql: '',
            status: 'error',
            error: errorMessage,
          };

          const qa: QuestionAnswer = {
            id: generateId(),
            question,
            result,
            timestamp: new Date(),
          };

          setQuestionAnswers((prev) => [qa, ...prev]);

          toast({
            title: 'Query failed',
            description: errorMessage,
            variant: 'destructive',
          });
        },
      }
    );
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Db Assistant</h1>
              <p className="text-sm text-muted-foreground">Ask questions about your database in natural language</p>
            </div>
            <div className="flex items-center gap-2">
              <Link href="/settings">
                <Button variant="outline" size="sm">
                  <Settings className="h-4 w-4 mr-2" />
                  Settings
                </Button>
              </Link>
              <Link href="/training">
                <Button variant="outline" size="sm">
                  Training
                </Button>
              </Link>
              <DarkModeToggle />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-5xl">
        <div className="space-y-8">
          {/* Question Input */}
          <div>
            <h2 className="text-lg font-semibold mb-4">Ask a Question</h2>
            <QuestionInput onSubmit={handleSubmit} isLoading={isPending} />
          </div>

          {/* Results */}
          {questionAnswers.length > 0 && (
            <div className="space-y-8">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">Results</h2>
                <button
                  onClick={() => setQuestionAnswers([])}
                  className="text-sm text-muted-foreground hover:text-foreground"
                >
                  Clear all
                </button>
              </div>
              
              {questionAnswers.map((qa) => (
                <QuestionAnswerCard
                  key={qa.id}
                  question={qa.question}
                  result={qa.result}
                  timestamp={qa.timestamp}
                />
              ))}
            </div>
          )}

          {/* Empty State */}
          {questionAnswers.length === 0 && !isPending && (
            <div className="text-center py-12">
              <p className="text-muted-foreground mb-4">
                Start by asking a question about your database
              </p>
              <div className="text-sm text-muted-foreground space-y-2">
                <p className="font-semibold">Example questions:</p>
                <ul className="space-y-1">
                  <li>• What are the top 10 customers by sales?</li>
                  <li>• Show me the monthly revenue for the last year</li>
                  <li>• Which products have the highest profit margin?</li>
                  <li>• List employees hired in the last 3 months</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
                <footer className="mt-8 pt-6 border-t text-center text-sm text-muted-foreground">
            <p>
              Powered by{' '}
              <a
                href="https://vanna.ai"
                target="_blank"
                rel="noopener noreferrer"
                className="underline hover:text-foreground"
              >
                Db Assistant
              </a>
            </p>
          </footer>
    </div>
  );
}
