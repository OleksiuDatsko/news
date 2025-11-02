export interface IUser {
  id: number;
  email: string;
  username: string;
  permissions: {
    no_ads: boolean;
    exclusive_content: boolean;
    save_article: boolean;
    comment: boolean;
  };
  created_at: string;
  savedArticles?: number[];
}