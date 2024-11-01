import { create } from "zustand";

const usePackageStore = create((set) => ({
  packageData: null,
  setPackageData: (data) => set({ packageData: data }),
  showPopup: false,
  setShowPopup: (value) => set({ showPopup: value }),
  deleteItem: (packageIndex, itemId) =>
    set((state) => {
      // Create a deep copy of the packages array
      const updatedPackages = [...state.packageData.packages];

      // Filter out the item with the specified itemId from the package
      updatedPackages[packageIndex].items = updatedPackages[
        packageIndex
      ].items.filter((item) => item.id !== itemId);

      updatedPackages[packageIndex].total_price = updatedPackages[
        packageIndex
      ].items.reduce((acc, item) => acc + item.price, 0);

      updatedPackages[packageIndex].remaining_budget =
        parseInt(state.packageData.budget) -
        parseInt(updatedPackages[packageIndex].total_price);

      // Update state with the modified packages
      return {
        packageData: {
          ...state.packageData,
          packages: updatedPackages,
        },
      };
    }),
}));

export default usePackageStore;
