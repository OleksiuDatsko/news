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
  preferences: {
    [key: string]: any
  }
  followed_authors?: number[];
}