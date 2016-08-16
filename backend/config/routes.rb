Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  root to: "prediction#index"
  resources :prefs
  resources :prediction do
    collection do
      get :fetch_prediction
    end
  end
end
