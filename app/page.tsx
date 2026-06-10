'use client';

import { useState } from 'react';
import { SplashScreen } from '@/app/components/SplashScreen';
import { Fase1AltarV2 } from '@/app/components/Fase1AltarV2';

export default function Home() {
  const [splashComplete, setSplashComplete] = useState(false);

  return (
    <>
      {!splashComplete && <SplashScreen onComplete={() => setSplashComplete(true)} />}
      {splashComplete && <Fase1AltarV2 />}
    </>
  );
}
