import React from "react";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  NavigationMenuViewport,
} from "@/components/ui/navigation-menu"

import Navbar from '../components/ui/navbar';

export default function Home() {
  const backgroundImageStyle = {
    backgroundImage: 'url("landing.jpeg")',
  };

  const blurOverlayStyle = {
    backdropFilter: "blur(5px)",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  };

  const redirectToApp = () => {
    window.location.href = "/app";
  };

  return (
    <div className="relative min-h-screen">
      <div className="absolute inset-0" style={blurOverlayStyle}></div>
        <div>
          <Navbar/>
        </div>
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-white text-center">
          <h1 className="text-4xl font-bold">your memories reimagined.</h1>
          <p className="mt-4 text-lg">
            no more deja vu. relive your memories in real time, with a simple
            search.
          </p>
          <button
            className="bg-white text-black px-4 py-2 rounded-lg mt-6 hover:bg-slate-100"
            onClick={redirectToApp}
          >
            Start now!
          </button>
        </div>
      </div>
    </div>
  );
}
