import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent) },
  { path: 'cpu', loadComponent: () => import('./pages/cpu.component').then(m => m.CpuComponent) },
  { path: 'memory', loadComponent: () => import('./pages/memory.component').then(m => m.MemoryComponent) },
  { path: 'storage', loadComponent: () => import('./pages/storage.component').then(m => m.StorageComponent) },
  { path: 'network', loadComponent: () => import('./pages/network.component').then(m => m.NetworkComponent) },
  { path: 'processes', loadComponent: () => import('./pages/processes.component').then(m => m.ProcessesComponent) },
  { path: 'settings', loadComponent: () => import('./pages/settings.component').then(m => m.SettingsComponent) },
  { path: '**', redirectTo: 'dashboard' }
];
