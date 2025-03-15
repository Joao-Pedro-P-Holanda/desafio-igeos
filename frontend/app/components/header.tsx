"use client"

import { NavLink } from "react-router"

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"
import { ModeToggle } from "./mode-toggle"

export function Header() {
  return (
    <header className="w-full flex flex-start p-2 bg-surface-container">
      <NavigationMenu className='w-full max-w-full justify-start'>
        <NavigationMenuList>
          <NavigationMenuItem>
            <NavLink to="/" >
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Dashboards
              </NavigationMenuLink>
            </NavLink>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
      <ModeToggle />
    </header>
  )
}

