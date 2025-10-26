import { Battery, Camera, Cpu, Monitor, Star } from 'lucide-react';
import type { PhoneDetails } from '../types/api.types';

interface PhoneListProps {
  phones: PhoneDetails[];
}

export function PhoneList({ phones }: PhoneListProps) {
  return (
    <div className="space-y-4">
      {phones.map((phone) => (
        <div
          key={phone.id}
          className="bg-white rounded-xl shadow-md overflow-hidden border border-gray-100 hover:shadow-lg transition-all hover:border-blue-300"
        >
          <div className="flex flex-col sm:flex-row">
            <div className="bg-gradient-to-br from-blue-500 to-cyan-500 p-6 sm:w-48 flex-shrink-0 flex flex-col justify-between">
              <div>
                <h4 className="text-lg font-bold text-white mb-1">{phone.name}</h4>
                <p className="text-blue-100 text-sm mb-3">{phone.brand}</p>
              </div>
              <div>
                <div className="text-2xl font-bold text-white">
                  ₹{phone.price.toLocaleString()}
                </div>
                <div className="flex items-center gap-1 mt-1">
                  <Star className="w-4 h-4 fill-yellow-300 text-yellow-300" />
                  <span className="text-white text-sm font-semibold">{phone.rating}</span>
                </div>
              </div>
            </div>

            <div className="flex-1 p-6">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
                <div className="flex items-center gap-2">
                  <Monitor className="w-4 h-4 text-blue-600" />
                  <div>
                    <div className="text-xs text-gray-500">Display</div>
                    <div className="text-sm font-semibold text-gray-900">
                      {phone.display_size_inch}"
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-green-600" />
                  <div>
                    <div className="text-xs text-gray-500">RAM</div>
                    <div className="text-sm font-semibold text-gray-900">{phone.ram_gb}GB</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Camera className="w-4 h-4 text-purple-600" />
                  <div>
                    <div className="text-xs text-gray-500">Camera</div>
                    <div className="text-sm font-semibold text-gray-900">
                      {phone.rear_camera_mp}MP
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Battery className="w-4 h-4 text-orange-600" />
                  <div>
                    <div className="text-xs text-gray-500">Battery</div>
                    <div className="text-sm font-semibold text-gray-900">
                      {phone.battery_mah}mAh
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap gap-2 mb-3">
                {phone.features.slice(0, 4).map((feature, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-xs font-medium"
                  >
                    {feature}
                  </span>
                ))}
              </div>

              <div className="flex items-center gap-2 text-xs text-gray-600">
                <span>{phone.processor}</span>
                <span className="text-gray-300">•</span>
                <span>{phone.os}</span>
                <span className="text-gray-300">•</span>
                <span>{phone.network}</span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
