"use client"

import { NavLink } from "react-router"

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Avatar,
  AvatarImage,
  AvatarFallback
} from "@/components/ui/avatar"
import { ModeToggle } from "./mode-toggle"
import { useAuth0 } from "@auth0/auth0-react"
import LoginButton from "./login-button"
import LogoutButton from "./logout-button"

export function Header() {
  const { user, isAuthenticated } = useAuth0()
  return (
    <header className="w-full flex flex-start p-2 bg-surface-container gap-2">
      <NavigationMenu className='w-full max-w-full justify-start'>
        <NavigationMenuList>
          <NavigationMenuItem>
            <NavLink to="/" className={navigationMenuTriggerStyle()}>
              Home
            </NavLink>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <NavLink to="/geracao-energia" className={navigationMenuTriggerStyle()}>
              Balanço de Energia
            </NavLink>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <NavLink to="/custos-energia" className={navigationMenuTriggerStyle()}>
              Custo Marginal de Operação
            </NavLink>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
      <ModeToggle />
      {isAuthenticated ?
        <DropdownMenu>
          <DropdownMenuTrigger>
            <Avatar>
              <AvatarImage src={user!.picture} alt={user!.name} />
              <AvatarFallback />
            </Avatar>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem>
              <LogoutButton />
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        : <LoginButton />}
    </header>
  )
}

