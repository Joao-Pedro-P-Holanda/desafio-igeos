// Icon.tsx

import { Loader2 } from 'lucide-react';

const Icons = {
  spinner: Loader2,
};

export function CircularProgress() {
  return <Icons.spinner className="h-4 w-4 animate-spin" />
} 
