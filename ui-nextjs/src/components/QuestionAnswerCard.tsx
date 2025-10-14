/**
 * Question answer card component
 * Combines SQL display, results table, and chart visualization
 */

'use client';

import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AlertCircle, Clock } from 'lucide-react';
import { SQLHighlight } from '@/components/SQLHighlight';
import { ResultsDisplay } from '@/components/ResultsDisplay';
import { ChartRenderer } from '@/components/ChartRenderer';
import { formatExecutionTime } from '@/lib/utils';
import type { QueryResult } from '@/lib/types';

interface QuestionAnswerCardProps {
  question: string;
  result: QueryResult;
  timestamp?: Date;
}

export function QuestionAnswerCard({ question, result, timestamp }: QuestionAnswerCardProps) {
  const isError = result.status === 'error';
  const executionTime = result.execution_time || result.executionTime;
  const figureId = result.figure_id || result.chartId;

  return (
    <div className="space-y-4">
      {/* Question */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <p className="text-lg font-semibold">{question}</p>
              {timestamp && (
                <p className="text-sm text-muted-foreground mt-1">
                  {timestamp.toLocaleString()}
                </p>
              )}
            </div>
            <div className="flex items-center gap-2">
              {executionTime && (
                <Badge variant="secondary" className="gap-1">
                  <Clock className="h-3 w-3" />
                  {formatExecutionTime(executionTime)}
                </Badge>
              )}
              <Badge variant={isError ? 'destructive' : 'default'}>
                {isError ? 'Error' : 'Success'}
              </Badge>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Error Message */}
      {isError && result.error && (
        <Card className="border-destructive">
          <CardContent className="pt-6">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-destructive mt-0.5" />
              <div>
                <p className="font-semibold text-destructive">Query Failed</p>
                <p className="text-sm text-muted-foreground mt-1">{result.error}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* SQL Query */}
      {result.sql && (
        <div>
          <h3 className="text-sm font-semibold mb-2">Generated SQL</h3>
          <SQLHighlight sql={result.sql} />
        </div>
      )}

      {/* Results Table */}
      {!isError && result.data && result.data.length > 0 && (
        <div>
          <ResultsDisplay
            data={result.data}
            columns={result.columnNames || (result.columns?.map(c => typeof c === 'string' ? c : c.name))}
          />
        </div>
      )}

      {/* Chart */}
      {!isError && figureId && (
        <div>
          <ChartRenderer figureId={figureId} />
        </div>
      )}

      {/* No Results */}
      {!isError && (!result.data || result.data.length === 0) && (
        <Card>
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">
              Query executed successfully but returned no results
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
