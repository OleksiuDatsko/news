import type { IAuthor } from '$lib/types/author';
import type { ICategory } from '$lib/types/category';

export interface IArticle {
  id: number;
  title: string;
  status: 'published' | 'draft' | 'archived';
  is_exclusive: boolean;
  is_breaking: boolean;
  views_count: number;
  created_at: string;
  author: IAuthor;
  category: ICategory | null;
  keywords: string[];
  is_saved?: boolean;
  is_liked?: boolean;
  likes_count?: number;
}

export interface IArticleFull extends IArticle {
  content: string;
}
