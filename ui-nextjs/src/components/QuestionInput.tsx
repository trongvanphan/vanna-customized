/**
 * Question input component
 * Textarea for natural language questions with submit button
 */

'use client';

import { useState } from 'react';
import { Loader2, Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { generateSessionId } from '@/lib/utils';

interface QuestionInputProps {
  onSubmit: (question: string, sessionId: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
}

export function QuestionInput({ onSubmit, isLoading = false, disabled = false }: QuestionInputProps) {
  const [question, setQuestion] = useState('');
  const [sessionId] = useState(() => generateSessionId());

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim() && !isLoading) {
      onSubmit(question.trim(), sessionId);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Submit on Enter (without Shift for new line)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (question.trim() && !isLoading) {
        onSubmit(question.trim(), sessionId);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-4">
      <div className="relative">
        <Textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your database... (e.g., 'What are the top 10 customers by sales?')"
          className="min-h-[100px] pr-12 resize-none"
          disabled={disabled || isLoading}
        />
        <div className="absolute bottom-3 right-3">
          <Button
            type="submit"
            size="icon"
            disabled={!question.trim() || isLoading || disabled}
            className="h-8 w-8"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>
      <p className="text-xs text-muted-foreground">
        Press <kbd className="px-1.5 py-0.5 text-xs border rounded bg-muted">Enter</kbd> to submit,{' '}
        <kbd className="px-1.5 py-0.5 text-xs border rounded bg-muted">Shift</kbd> +{' '}
        <kbd className="px-1.5 py-0.5 text-xs border rounded bg-muted">Enter</kbd> for new line
      </p>
    </form>
  );
}
