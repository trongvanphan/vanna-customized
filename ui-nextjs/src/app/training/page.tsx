/**
 * Training page - Manage training data
 */

'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Loader2, Upload, BookOpen } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { loadTrainingData } from '@/lib/api-client';
import type { TrainingDataLoadResult } from '@/lib/types';
import Link from 'next/link';

export default function TrainingPage() {
  const { toast } = useToast();
  const [lastResult, setLastResult] = useState<TrainingDataLoadResult | null>(null);

  const loadDataMutation = useMutation({
    mutationFn: loadTrainingData,
    onSuccess: (result: TrainingDataLoadResult) => {
      setLastResult(result);
      toast({
        title: 'Success',
        description: result.message,
      });
    },
    onError: (error: Error) => {
      toast({
        title: 'Error',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <BookOpen className="h-6 w-6" />
            <h1 className="text-3xl font-bold">Training Data</h1>
          </div>
          <Link href="/">
            <Button variant="outline">Back to Home</Button>
          </Link>
        </div>
        <p className="text-muted-foreground">
          Load training data (DDL, documentation, and Q&A pairs) into the vector store
        </p>
      </div>

      <div className="space-y-6">
        {/* Load Training Data Card */}
        <Card>
          <CardHeader>
            <CardTitle>Load Training Data</CardTitle>
            <CardDescription>
              Load DDL schemas, documentation, and training Q&A pairs from the configured directory
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-md border p-4 space-y-2">
              <h3 className="font-semibold text-sm">What gets loaded:</h3>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                <li><strong>DDL Files</strong>: Database schema definitions (.sql files)</li>
                <li><strong>Documentation</strong>: Business rules and definitions (.md files)</li>
                <li><strong>Training Pairs</strong>: Example questions and SQL queries (.json files)</li>
              </ul>
            </div>

            <Button 
              onClick={() => loadDataMutation.mutate()} 
              disabled={loadDataMutation.isPending}
              className="w-full"
            >
              {loadDataMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : (
                <Upload className="h-4 w-4 mr-2" />
              )}
              {loadDataMutation.isPending ? 'Loading...' : 'Load Training Data'}
            </Button>

            {lastResult && (
              <div className="rounded-md border p-4 space-y-2">
                <h3 className="font-semibold text-sm">Last Load Results:</h3>
                <div className="text-sm space-y-1">
                  {lastResult.stats && (
                    <>
                      <p>✅ DDL Files: {lastResult.stats.ddl_loaded || 0}</p>
                      <p>✅ Documentation: {lastResult.stats.docs_loaded || 0}</p>
                      <p>✅ Training Pairs: {lastResult.stats.pairs_loaded || 0}</p>
                      {lastResult.stats.errors && lastResult.stats.errors.length > 0 && (
                        <div className="mt-2 text-destructive">
                          <p>⚠️ Errors: {lastResult.stats.errors.length}</p>
                          <ul className="list-disc list-inside ml-4">
                            {lastResult.stats.errors.map((error, idx) => (
                              <li key={idx}>{error}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Training Configuration Info */}
        <Card>
          <CardHeader>
            <CardTitle>Configuration</CardTitle>
            <CardDescription>
              Training data location and settings (configured in Settings page)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-sm space-y-2">
              <p className="text-muted-foreground">
                Training data is loaded from the path configured in the Training tab of the Settings page.
              </p>
              <p className="text-muted-foreground">
                By default, it loads from <code className="px-1 py-0.5 bg-muted rounded">../trainingMyDb/</code> directory:
              </p>
              <ul className="list-disc list-inside ml-4 text-muted-foreground space-y-1">
                <li><code className="px-1 py-0.5 bg-muted rounded">ddl/</code> - SQL schema files</li>
                <li><code className="px-1 py-0.5 bg-muted rounded">documentation/</code> - Markdown documentation</li>
                <li><code className="px-1 py-0.5 bg-muted rounded">trainingpairs/</code> - JSON Q&A files</li>
              </ul>
              <div className="mt-4">
                <Link href="/settings?tab=training">
                  <Button variant="outline" size="sm">
                    Go to Settings → Training
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* How It Works */}
        <Card>
          <CardHeader>
            <CardTitle>How Training Works</CardTitle>
            <CardDescription>
              Understanding the RAG (Retrieval-Augmented Generation) approach
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-sm space-y-3">
              <div>
                <h4 className="font-semibold mb-1">1. Training Phase (This Page)</h4>
                <p className="text-muted-foreground">
                  Load your database schema (DDL), business documentation, and example Q&A pairs into a vector database. 
                  This data is converted to embeddings for semantic search.
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold mb-1">2. Query Phase (Home Page)</h4>
                <p className="text-muted-foreground">
                  When you ask a question, the system retrieves the most relevant DDL, documentation, and example queries 
                  from the vector store and includes them in the prompt to the LLM.
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold mb-1">3. Generation Phase</h4>
                <p className="text-muted-foreground">
                  The LLM uses the retrieved context plus your question to generate accurate SQL queries that match 
                  your specific database schema and business rules.
                </p>
              </div>

              <div className="mt-4 p-3 bg-muted rounded-md">
                <p className="text-xs">
                  <strong>Tip:</strong> The more training data you provide (especially example Q&A pairs), 
                  the better the SQL generation quality. Update training data whenever your schema changes.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
