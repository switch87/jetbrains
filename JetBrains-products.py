from PackageLister import PackageList

package_list = PackageList("https://www.jetbrains.com/updates/updates.xml")
package_list.print_tree()
print('Packages: '+ str(package_list.package_count()))
print('Channels: '+ str(package_list.all_channels_count()))