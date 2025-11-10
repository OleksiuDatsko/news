export interface ISubscriptionPlan {
  id: number;
  name: string;
  price_per_month: number;
  description: string;
  permissions: {
    no_ads: boolean;
    exclusive_content: boolean;
    save_article: boolean;
    comment: boolean;
  };
}
