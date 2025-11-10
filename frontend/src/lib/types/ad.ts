export interface IAd {
  id: number;
  title: string;
  content: string | null;
  ad_type: 'banner' | 'sidebar' | 'popup' | 'inline' | 'video';
}
