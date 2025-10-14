/**
 * SQL syntax highlighting component
 * Uses Prism.js for syntax highlighting with copy button
 */

'use client';

import { useEffect, useRef, useState } from 'react';
import { Check, Copy } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

// Dynamically import Prism.js on client side
import Prism from 'prismjs';
import 'prismjs/components/prism-sql';
import 'prismjs/plugins/line-numbers/prism-line-numbers';
import 'prismjs/plugins/line-numbers/prism-line-numbers.css';

interface SQLHighlightProps {
  sql: string;
  showLineNumbers?: boolean;
  className?: string;
}

export function SQLHighlight({ sql, showLineNumbers = true, className = '' }: SQLHighlightProps) {
  const codeRef = useRef<HTMLElement>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (codeRef.current) {
      Prism.highlightElement(codeRef.current);
    }
  }, [sql]);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card className={`relative ${className}`}>
      <div className="absolute top-2 right-2 z-10">
        <Button
          variant="ghost"
          size="icon"
          onClick={handleCopy}
          className="h-8 w-8"
          aria-label="Copy SQL"
        >
          {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
        </Button>
      </div>
      <pre className={showLineNumbers ? 'line-numbers' : ''}>
        <code ref={codeRef} className="language-sql">
          {sql}
        </code>
      </pre>
    </Card>
  );
}
