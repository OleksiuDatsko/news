export interface ICategory {
  id: number;
  name: string;
  description: string | null;
  slug: string;
  is_searchable: boolean;
  total_articles: number;
}
